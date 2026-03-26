<script>
  export let loading = false;
  export let includeMessage = false;
  export let enableTimer = false;
  export let canShare = false;
  export let onEncrypt = () => {};
  export let onShare = () => {};
</script>

<div class="flex flex-col gap-3 sm:flex-row">
  <button class="btn-primary flex-1" on:click={onEncrypt} disabled={loading}>
    {loading ? "Encrypting..." : "Encrypt image"}
  </button>
  <button class="btn-secondary flex-1" on:click={onShare} disabled={!canShare || loading}>
    Share
  </button>
</div>

<div class="mt-3 text-xs text-slate-500">
  {#if includeMessage}
    Hidden-message embedding is enabled.
  {/if}
  {#if includeMessage && enableTimer}
    &nbsp;
  {/if}
  {#if enableTimer}
    Self-destruct timer will be applied on share.
  {/if}
</div>
