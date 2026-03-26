<script>
  export let title = "Result";
  export let message = "";
  export let type = "info";
  export let imageUrl = "";
  export let downloadUrl = "";
  export let filename = "";

  const toneMap = {
    info: "border-sky-200 bg-sky-50 text-sky-900",
    success: "border-emerald-200 bg-emerald-50 text-emerald-900",
    warning: "border-amber-200 bg-amber-50 text-amber-900",
    error: "border-rose-200 bg-rose-50 text-rose-900"
  };
</script>

<div class={`panel p-6 ${toneMap[type] || toneMap.info} dark:border-white/10`}>
  <h3 class="font-display text-lg font-semibold">{title}</h3>
  {#if message}
    <p class="mt-2 whitespace-pre-line text-sm leading-6">{message}</p>
  {/if}

  {#if imageUrl}
    <img class="mt-4 max-h-80 w-full rounded-3xl object-contain ring-1 ring-black/5" src={imageUrl} alt={title} />
  {/if}

  {#if downloadUrl}
    <div class="mt-4">
      <a class="btn-secondary" href={downloadUrl} download={filename}>Download</a>
    </div>
  {/if}
</div>
