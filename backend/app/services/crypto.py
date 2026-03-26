import hashlib

import numpy as np
from PIL import Image


class DNAUtils:
    @staticmethod
    def pixel_to_dna(image_array):
        dna_seq = np.zeros(image_array.shape + (4,), dtype=np.uint8)
        dna_seq[..., 0] = (image_array >> 6) & 3
        dna_seq[..., 1] = (image_array >> 4) & 3
        dna_seq[..., 2] = (image_array >> 2) & 3
        dna_seq[..., 3] = image_array & 3
        return dna_seq

    @staticmethod
    def dna_to_pixel(dna_seq):
        pixel_array = (
            (dna_seq[..., 0] << 6)
            | (dna_seq[..., 1] << 4)
            | (dna_seq[..., 2] << 2)
            | dna_seq[..., 3]
        )
        return pixel_array.astype(np.uint8)

    @staticmethod
    def dna_xor_operation(dna_img, dna_key):
        return np.bitwise_xor(dna_img, dna_key)

    @staticmethod
    def dna_complement_operation(dna_seq, control_key):
        mask = (control_key % 4) >= 2
        out_seq = dna_seq.copy()
        out_seq[mask] = 3 - out_seq[mask]
        return out_seq

    @staticmethod
    def dna_add_operation(dna_img, dna_key):
        return (dna_img + dna_key) % 4


class SteganographyUtils:
    @staticmethod
    def text_to_dna(text):
        msg_bytes = text.encode("utf-8")
        length = len(msg_bytes)
        if length > 65535:
            raise ValueError("Message too long (max 65535 bytes)")
        header = []
        for i in range(7, -1, -1):
            header.append((length >> (i * 2)) & 3)
        body = []
        for byte in msg_bytes:
            body.append((byte >> 6) & 3)
            body.append((byte >> 4) & 3)
            body.append((byte >> 2) & 3)
            body.append(byte & 3)
        return np.array(header + body, dtype=np.uint8)

    @staticmethod
    def dna_to_text(dna_bases):
        length = 0
        for i in range(8):
            length = (length << 2) | int(dna_bases[i])
        if length == 0:
            return None
        msg_bytes = bytearray()
        offset = 8
        for i in range(length):
            idx = offset + i * 4
            byte = (
                (int(dna_bases[idx]) << 6)
                | (int(dna_bases[idx + 1]) << 4)
                | (int(dna_bases[idx + 2]) << 2)
                | int(dna_bases[idx + 3])
            )
            msg_bytes.append(byte)
        return msg_bytes.decode("utf-8", errors="replace")

    @staticmethod
    def embed_message(dna_array, text):
        dna_msg = SteganographyUtils.text_to_dna(text)
        flat = dna_array.flatten()
        if len(dna_msg) > len(flat):
            raise ValueError(
                f"Message too large for this image ({len(dna_msg)} bases needed, {len(flat)} available)"
            )
        flat[: len(dna_msg)] = dna_msg
        return flat.reshape(dna_array.shape)

    @staticmethod
    def extract_message(dna_array):
        flat = dna_array.flatten()
        try:
            return SteganographyUtils.dna_to_text(flat)
        except Exception:
            return None


def generate_hyper_chaotic_sequence(length, r, beta, lambda_val, x0):
    x_seq = np.zeros(length)
    x = x0
    pi = np.pi
    for i in range(length):
        base_term = (r * x * (1 - x)) + (beta * (np.sin(pi * x) ** 2))
        x_next = (lambda_val * base_term) % 1
        x_seq[i] = x_next
        x = x_next
    return x_seq


def _build_encryption_artifacts(image_path, x0_base, r, beta, lambda_val, hidden_message=None):
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    height, width, channels = image_array.shape
    total_pixels = height * width * channels

    image_sum = np.sum(image_array)
    image_hash = image_sum / (total_pixels * 255)
    x0_dynamic = (x0_base + image_hash) % 1

    chaotic_seq1 = generate_hyper_chaotic_sequence(total_pixels, r, beta, lambda_val, x0_dynamic)
    chaotic_seq2 = generate_hyper_chaotic_sequence(total_pixels, beta, r, lambda_val, 1 - x0_dynamic)

    key_stream1 = (np.floor(chaotic_seq1 * 10**14) % 256).astype(np.uint8)
    key_matrix1 = key_stream1.reshape(height, width, channels)
    key_stream2 = (np.floor(chaotic_seq2 * 10**14) % 256).astype(np.uint8)
    key_matrix2 = key_stream2.reshape(height, width, channels)

    dna_img = DNAUtils.pixel_to_dna(image_array)
    dna_key1 = DNAUtils.pixel_to_dna(key_matrix1)
    dna_key2 = DNAUtils.pixel_to_dna(key_matrix2)

    if hidden_message:
        dna_img = SteganographyUtils.embed_message(dna_img, hidden_message)

    integrity_array = DNAUtils.dna_to_pixel(dna_img)

    dna_xor1 = DNAUtils.dna_xor_operation(dna_img, dna_key1)
    dna_comp1 = DNAUtils.dna_complement_operation(dna_xor1, dna_key1)
    dna_add = DNAUtils.dna_add_operation(dna_comp1, dna_key2)
    dna_xor2 = DNAUtils.dna_xor_operation(dna_add, dna_key2)
    dna_final = DNAUtils.dna_complement_operation(dna_xor2, dna_key2)

    intermediate1 = DNAUtils.dna_to_pixel(dna_comp1)
    encrypted_array = DNAUtils.dna_to_pixel(dna_final)

    return {
        "image_array": image_array,
        "key_matrix1": key_matrix1,
        "key_matrix2": key_matrix2,
        "intermediate1": intermediate1,
        "encrypted_array": encrypted_array,
        "integrity_array": integrity_array,
    }


def encrypt_image_robust(image_path, x0_base, r, beta, lambda_val, output_path, key_path, hidden_message=None):
    artifacts = _build_encryption_artifacts(image_path, x0_base, r, beta, lambda_val, hidden_message)
    Image.fromarray(artifacts["encrypted_array"]).save(output_path, "PNG")
    np.savez(key_path, key1=artifacts["key_matrix1"], key2=artifacts["key_matrix2"])
    return output_path, key_path


def encrypt_with_visualization(image_path, x0_base, r, beta, lambda_val, output_path, key_path, hidden_message=None):
    artifacts = _build_encryption_artifacts(image_path, x0_base, r, beta, lambda_val, hidden_message)
    Image.fromarray(artifacts["encrypted_array"]).save(output_path, "PNG")
    np.savez(key_path, key1=artifacts["key_matrix1"], key2=artifacts["key_matrix2"])

    stage_images = {
        "original": artifacts["image_array"],
        "key_preview": artifacts["key_matrix1"],
        "first_diffusion": artifacts["intermediate1"],
        "encrypted": artifacts["encrypted_array"],
    }

    return output_path, key_path, stage_images


def decrypt_image_robust(enc_path, key_path, output_path):
    enc_image = Image.open(enc_path)
    enc_array = np.array(enc_image)

    try:
        keys = np.load(key_path)
        key_matrix1 = keys["key1"]
        key_matrix2 = keys["key2"]
    except Exception:
        key_matrix = np.load(key_path)
        key_matrix1 = key_matrix
        key_matrix2 = key_matrix

    dna_enc = DNAUtils.pixel_to_dna(enc_array)
    dna_key1 = DNAUtils.pixel_to_dna(key_matrix1)
    dna_key2 = DNAUtils.pixel_to_dna(key_matrix2)

    dna_rev_f = DNAUtils.dna_complement_operation(dna_enc, dna_key2)
    dna_rev_e = DNAUtils.dna_xor_operation(dna_rev_f, dna_key2)
    dna_rev_d = (dna_rev_e - dna_key2) % 4
    dna_rev_c = DNAUtils.dna_complement_operation(dna_rev_d, dna_key1)
    dna_original = DNAUtils.dna_xor_operation(dna_rev_c, dna_key1)

    decrypted_array = DNAUtils.dna_to_pixel(dna_original)
    hidden_message = SteganographyUtils.extract_message(dna_original)
    Image.fromarray(decrypted_array).save(output_path, "PNG")
    return output_path, hidden_message


def compute_original_hash(image_path) -> str:
    image = Image.open(image_path).convert("RGB")
    return hashlib.sha256(np.array(image).tobytes()).hexdigest()


def compute_integrity_hash(image_path, hidden_message=None) -> str:
    if not hidden_message:
        return compute_original_hash(image_path)

    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    dna_img = DNAUtils.pixel_to_dna(image_array)
    dna_img = SteganographyUtils.embed_message(dna_img, hidden_message)
    integrity_array = DNAUtils.dna_to_pixel(dna_img)
    return hashlib.sha256(integrity_array.tobytes()).hexdigest()
