<script>
  export let labels = [];
  export let original = [];
  export let encrypted = [];

  const bucketCount = 32;

  function bucketize(values) {
    const size = Math.ceil(values.length / bucketCount);
    const buckets = [];
    for (let index = 0; index < bucketCount; index += 1) {
      const start = index * size;
      const end = Math.min(values.length, start + size);
      const sum = values.slice(start, end).reduce((total, value) => total + value, 0);
      buckets.push(sum);
    }
    return buckets;
  }

  $: originalBuckets = bucketize(original);
  $: encryptedBuckets = bucketize(encrypted);
  $: maxValue = Math.max(1, ...originalBuckets, ...encryptedBuckets);
</script>

<div class="panel p-6">
  <div class="flex items-start justify-between gap-4">
    <div>
      <h3 class="font-display text-lg font-semibold">Histogram Analysis</h3>
      <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">
        Aggregated pixel intensity distribution before and after encryption. Flatter encrypted buckets indicate stronger statistical diffusion.
      </p>
    </div>
    <div class="flex gap-4 text-xs text-slate-500 dark:text-slate-400">
      <span class="flex items-center gap-2"><span class="h-2.5 w-2.5 rounded-full bg-cyan-400"></span> Original</span>
      <span class="flex items-center gap-2"><span class="h-2.5 w-2.5 rounded-full bg-violet"></span> Encrypted</span>
    </div>
  </div>

  <div class="mt-6 grid gap-2" style="grid-template-columns: repeat(32, minmax(0, 1fr));">
    {#each originalBuckets as bucket, index}
      <div class="flex h-40 items-end gap-1">
        <div class="w-1/2 rounded-t-full bg-cyan-400/80" style={`height:${Math.max(6, (bucket / maxValue) * 100)}%`}></div>
        <div class="w-1/2 rounded-t-full bg-violet/80" style={`height:${Math.max(6, (encryptedBuckets[index] / maxValue) * 100)}%`}></div>
      </div>
    {/each}
  </div>

  <div class="mt-4 flex justify-between text-[11px] uppercase tracking-[0.24em] text-slate-400 dark:text-slate-500">
    <span>0</span>
    <span>Pixel intensity</span>
    <span>255</span>
  </div>
</div>
