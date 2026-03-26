<script>
  export let title = "";
  export let src = "";
  export let alt = "";
  export let emptyLabel = "Nothing to preview yet.";
</script>

<div class="panel p-6">
  <div class="mb-4 flex items-center justify-between">
    <h3 class="font-display text-lg font-semibold">{title}</h3>
  </div>

  {#if src}
    <img class="max-h-[26rem] w-full rounded-3xl object-contain ring-1 ring-slate-200" src={src} alt={alt || title} />
  {:else}
    <div class="flex min-h-64 items-center justify-center rounded-3xl border border-dashed border-slate-200 bg-slate-50 text-sm text-slate-500 dark:border-slate-700 dark:bg-slate-800/60 dark:text-slate-400">
      {emptyLabel}
    </div>
  {/if}
</div>
