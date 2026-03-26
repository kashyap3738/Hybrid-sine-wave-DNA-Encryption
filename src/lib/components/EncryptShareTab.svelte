<script>
  import Controls from "./Controls.svelte";
  import EncryptionVisualizer from "./EncryptionVisualizer.svelte";
  import ImageUpload from "./ImageUpload.svelte";
  import Preview from "./Preview.svelte";
  import ResultDisplay from "./ResultDisplay.svelte";
  import { api, getMediaUrl } from "../api.js";

  export let users = [];
  export let onRefresh = async () => {};

  let file = null;
  let previewUrl = "";
  let result = null;
  let message = "";
  let messageTone = "info";
  let x0 = 0.654321;
  let r = 3.99;
  let beta = 3.0;
  let lambdaVal = 500;
  let includeMessage = false;
  let hiddenMessage = "";
  let receiverId = "";
  let enableTimer = false;
  let viewDuration = 10;
  let visualizing = false;
  let actionLoading = false;

  function handleSelect(selectedFile) {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    file = selectedFile;
    previewUrl = file ? URL.createObjectURL(file) : "";
    result = null;
    message = "";
  }

  async function handleEncrypt() {
    if (!file) return;

    message = "";
    messageTone = "info";
    result = null;
    visualizing = true;
    actionLoading = true;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("x0", String(x0));
    formData.append("r", String(r));
    formData.append("beta", String(beta));
    formData.append("lambda_val", String(lambdaVal));
    if (includeMessage && hiddenMessage) {
      formData.append("hidden_message", hiddenMessage);
    }

    try {
      result = await api.encrypt(formData);
      message = includeMessage && hiddenMessage
        ? `Image encrypted successfully. Hidden message embedded (${hiddenMessage.length} characters).`
        : "Image encrypted successfully.";
      messageTone = "success";
      await onRefresh();
    } catch (error) {
      result = { error: error.message };
      message = "";
    } finally {
      actionLoading = false;
      setTimeout(() => {
        visualizing = false;
      }, 3200);
    }
  }

  async function handleShare() {
    if (!result?.image_id || !receiverId) return;
    actionLoading = true;

    try {
      await api.share({
        image_id: result.image_id,
        receiver_id: Number(receiverId),
        view_duration: enableTimer ? Number(viewDuration) : null
      });
      message = `Shared successfully${enableTimer ? ` with ${viewDuration}s self-destruct timer` : ""}.`;
      messageTone = "success";
      await onRefresh();
    } catch (error) {
      message = error.message;
      messageTone = "error";
    } finally {
      actionLoading = false;
    }
  }
</script>

<div class="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
  <ImageUpload {file} {previewUrl} onSelect={handleSelect} />

  <div class="panel p-6">
    <h3 class="font-display text-lg font-semibold">Encryption parameters</h3>
    <div class="mt-4 grid gap-4 sm:grid-cols-2">
      <div>
        <label class="label">Seed (x0)</label>
        <input class="input" type="number" min="0" max="1" step="0.000001" bind:value={x0} />
      </div>
      <div>
        <label class="label">Chaos (r)</label>
        <input class="input" type="number" min="3.6" max="4" step="0.01" bind:value={r} />
      </div>
      <div>
        <label class="label">Wave (beta)</label>
        <input class="input" type="number" min="0" max="5" step="0.1" bind:value={beta} />
      </div>
      <div>
        <label class="label">Zoom factor (lambda)</label>
        <input class="input" type="number" min="100" max="10000" step="1" bind:value={lambdaVal} />
      </div>
    </div>

    <div class="soft-card mt-6">
      <label class="flex items-center gap-3 text-sm font-medium text-slate-700 dark:text-slate-300">
        <input type="checkbox" bind:checked={includeMessage} />
        Include a hidden message
      </label>

      {#if includeMessage}
        <textarea class="input mt-4 min-h-28" placeholder="Type your secret message here..." bind:value={hiddenMessage}></textarea>
      {/if}
    </div>

    <div class="soft-card mt-6">
      <h4 class="text-sm font-semibold text-slate-900 dark:text-slate-100">Share with a user</h4>
      <div class="mt-4 grid gap-4 sm:grid-cols-2">
        <div>
          <label class="label">Recipient</label>
          <select class="input" bind:value={receiverId}>
            <option value="">Select recipient</option>
            {#each users as user}
              <option value={user.user_id}>{user.username}</option>
            {/each}
          </select>
        </div>
        <div>
          <label class="label">Self-destruct timer</label>
          <div class="flex h-[52px] items-center rounded-2xl border border-slate-200 bg-white px-4 dark:border-slate-700 dark:bg-slate-950/80">
            <input type="checkbox" bind:checked={enableTimer} />
            <span class="ml-3 text-sm text-slate-600 dark:text-slate-300">Enable timer</span>
          </div>
        </div>
      </div>

      {#if enableTimer}
        <div class="mt-4">
          <label class="label">View duration (seconds)</label>
          <input class="input" type="number" min="1" max="300" step="1" bind:value={viewDuration} />
        </div>
      {/if}
    </div>

    <div class="mt-6">
      <Controls
        loading={actionLoading}
        {includeMessage}
        {enableTimer}
        canShare={Boolean(result?.image_id && receiverId)}
        onEncrypt={handleEncrypt}
        onShare={handleShare}
      />
    </div>
  </div>
</div>

{#if message}
  <div class="mt-6">
    <ResultDisplay title="Status" type={messageTone} message={message} />
  </div>
{/if}

{#if result?.visualization}
  <div class="mt-6">
    <EncryptionVisualizer visualization={result.visualization} playing={visualizing} />
  </div>
{/if}

{#if result?.encrypted_url}
  <div class="mt-6 grid gap-6 xl:grid-cols-2">
    <Preview title="Original preview" src={previewUrl} alt="Original image" emptyLabel="Upload an image to start." />
    <ResultDisplay
      title="Encrypted result"
      type="success"
      message={includeMessage && hiddenMessage ? `Hidden message embedded (${hiddenMessage.length} characters).` : "Image encrypted successfully."}
      imageUrl={getMediaUrl(result.encrypted_url)}
      downloadUrl={getMediaUrl(result.encrypted_url)}
      filename={result.filename}
    />
  </div>
{:else if result?.error}
  <div class="mt-6">
    <ResultDisplay title="Encryption failed" type="error" message={result.error} />
  </div>
{/if}
