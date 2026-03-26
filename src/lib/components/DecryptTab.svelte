<script>
  import { onDestroy } from "svelte";
  import Preview from "./Preview.svelte";
  import ResultDisplay from "./ResultDisplay.svelte";
  import { api, getMediaUrl } from "../api.js";

  export let shares = [];

  let selectedShareId = "";
  let decryptResult = null;
  let decryptError = "";
  let decrypting = false;
  let remaining = 0;
  let timer = null;

  $: selectedShare = shares.find((share) => String(share.share_id) === String(selectedShareId)) || null;
  $: if (selectedShareId && decryptResult && String(decryptResult.share_id) !== String(selectedShareId)) {
    clearTimer();
    decryptResult = null;
    decryptError = "";
    remaining = 0;
  }

  function clearTimer() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  function startCountdown(expiresAt) {
    clearTimer();
    if (!expiresAt) {
      remaining = 0;
      return;
    }
    remaining = Math.max(0, expiresAt - Math.floor(Date.now() / 1000));
    timer = setInterval(() => {
      remaining = Math.max(0, expiresAt - Math.floor(Date.now() / 1000));
      if (remaining <= 0) {
        clearTimer();
        decryptResult = null;
        decryptError = "Self-Destruct triggered. This image has been permanently erased.";
      }
    }, 1000);
  }

  async function handleDecrypt() {
    if (!selectedShareId) return;
    decrypting = true;
    decryptError = "";

    try {
      decryptResult = await api.decryptShare(Number(selectedShareId));
      startCountdown(decryptResult.expires_at);
    } catch (error) {
      decryptResult = null;
      decryptError = error.message;
    } finally {
      decrypting = false;
    }
  }

  onDestroy(() => {
    clearTimer();
  });
</script>

<div class="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
  <div class="panel p-6">
    <label class="label">Select image</label>
    <select class="input" bind:value={selectedShareId}>
      <option value="">Choose image</option>
      {#each shares as share}
        <option value={share.share_id}>{share.filename} - from {share.sender}</option>
      {/each}
    </select>

    {#if selectedShare}
      <div class="soft-card mt-5 space-y-2 text-sm text-slate-600 dark:text-slate-300">
        <div><span class="font-semibold text-slate-900 dark:text-slate-100">File:</span> {selectedShare.filename}</div>
        <div><span class="font-semibold text-slate-900 dark:text-slate-100">From:</span> {selectedShare.sender}</div>
        {#if selectedShare.view_duration}
          <div><span class="font-semibold text-slate-900 dark:text-slate-100">Self-destruct:</span> {selectedShare.view_duration}s after decryption</div>
        {/if}
        {#if selectedShare.is_expired === 1}
          <div class="font-semibold text-rose-600">Self-Destructed: Time expired.</div>
        {/if}
      </div>
    {/if}

    <button class="btn-primary mt-6 w-full" disabled={!selectedShareId || selectedShare?.is_expired === 1 || decrypting} on:click={handleDecrypt}>
      {decrypting ? "Decrypting..." : "Decrypt"}
    </button>
  </div>

  <Preview title="Encrypted image" src={selectedShare ? getMediaUrl(selectedShare.encrypted_url) : ""} alt="Encrypted preview" emptyLabel="Choose a shared image to inspect." />
</div>

{#if decryptError}
  <div class="mt-6">
    <ResultDisplay title="Decrypt status" type="error" message={decryptError} />
  </div>
{/if}

{#if decryptResult}
  <div class="mt-6 grid gap-6 xl:grid-cols-2">
    <ResultDisplay
      title="Decrypted image"
      type="success"
      message={remaining > 0 ? `Self-destruct countdown: ${remaining}s remaining.` : "Decrypted successfully."}
      imageUrl={getMediaUrl(decryptResult.decrypted_url)}
      downloadUrl={getMediaUrl(decryptResult.decrypted_url)}
      filename={`decrypted_${decryptResult.filename}`}
    />

    {#if decryptResult.has_hidden_msg && decryptResult.hidden_message}
      <ResultDisplay title="Hidden message extracted" type="info" message={decryptResult.hidden_message} />
    {:else}
      <ResultDisplay title="Hidden message extracted" type="info" message="No hidden message was extracted from this image." />
    {/if}
  </div>
{/if}
