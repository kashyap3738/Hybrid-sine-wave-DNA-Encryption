<script>
  export let labels = [];
  export let original = [];
  export let encrypted = [];

  const width = 900;
  const height = 320;
  const padding = 28;

  $: maxValue = Math.max(1, ...original, ...encrypted);
  $: pointsOriginal = labels
    .map((label, index) => {
      const x = padding + (index / Math.max(1, labels.length - 1)) * (width - padding * 2);
      const y = height - padding - (original[index] / maxValue) * (height - padding * 2);
      return `${x},${y}`;
    })
    .join(" ");
  $: pointsEncrypted = labels
    .map((label, index) => {
      const x = padding + (index / Math.max(1, labels.length - 1)) * (width - padding * 2);
      const y = height - padding - (encrypted[index] / maxValue) * (height - padding * 2);
      return `${x},${y}`;
    })
    .join(" ");
</script>

<div class="panel p-6">
  <div class="mb-4 flex items-center justify-between">
    <h3 class="font-display text-lg font-semibold">Pixel Distribution</h3>
    <div class="flex gap-4 text-xs text-slate-500">
      <span class="flex items-center gap-2"><span class="h-2 w-2 rounded-full bg-sky-400"></span> Original</span>
      <span class="flex items-center gap-2"><span class="h-2 w-2 rounded-full bg-coral"></span> Encrypted</span>
    </div>
  </div>

  <svg viewBox={`0 0 ${width} ${height}`} class="w-full overflow-visible rounded-3xl bg-slate-50">
    <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#cbd5e1" stroke-width="1" />
    <line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="#cbd5e1" stroke-width="1" />
    <polyline fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" points={pointsOriginal} />
    <polyline fill="none" stroke="#ff6b57" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" points={pointsEncrypted} />
  </svg>
</div>
