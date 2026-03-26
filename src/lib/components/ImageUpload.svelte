<script>
  export let file = null;
  export let previewUrl = "";
  export let accept = "image/png,image/jpeg";
  export let onSelect = () => {};

  function handleChange(event) {
    const selected = event.currentTarget.files?.[0] || null;
    onSelect(selected);
  }
</script>

<div class="panel p-6">
  <label class="label" for="file-upload">Choose an image to encrypt</label>
  <input id="file-upload" class="input file:mr-4 file:rounded-xl file:border-0 file:bg-ink file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white" type="file" accept={accept} on:change={handleChange} />

  {#if file}
    <div class="mt-4 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600 dark:border-slate-700 dark:bg-slate-800/70 dark:text-slate-300">
      <div class="font-semibold text-slate-900 dark:text-slate-100">{file.name}</div>
      <div>{Math.round(file.size / 1024)} KB</div>
    </div>
  {/if}

  {#if previewUrl}
    <img class="mt-5 max-h-72 w-full rounded-3xl object-contain ring-1 ring-slate-200" src={previewUrl} alt="Selected preview" />
  {/if}
</div>
