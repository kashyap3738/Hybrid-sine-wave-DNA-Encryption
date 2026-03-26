<script>
  export let comparison = null;

  const metrics = [
    {
      key: "mean",
      title: "Mean intensity",
      hint: "Average brightness across all channels.",
      originalKey: "original_mean",
      encryptedKey: "encrypted_mean"
    },
    {
      key: "std",
      title: "Standard deviation",
      hint: "Spread of pixel values.",
      originalKey: "original_std",
      encryptedKey: "encrypted_std"
    }
  ];

  function format(value) {
    return Number(value || 0).toFixed(2);
  }
</script>

<div class="panel p-6">
  <h3 class="font-display text-lg font-semibold">Before vs After Encryption</h3>
  <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">
    These paired bars compare the original and encrypted images using simple descriptive statistics without changing the encryption pipeline.
  </p>

  <div class="mt-6 space-y-6">
    {#each metrics as metric}
      {@const originalValue = comparison?.[metric.originalKey] || 0}
      {@const encryptedValue = comparison?.[metric.encryptedKey] || 0}
      {@const maxValue = Math.max(originalValue, encryptedValue, 1)}
      <div>
        <div class="flex items-center justify-between text-sm">
          <div>
            <div class="font-semibold text-slate-900 dark:text-slate-100">{metric.title}</div>
            <div class="text-slate-500 dark:text-slate-400">{metric.hint}</div>
          </div>
          <div class="text-right text-slate-500 dark:text-slate-400">
            <div>O: {format(originalValue)}</div>
            <div>E: {format(encryptedValue)}</div>
          </div>
        </div>
        <div class="mt-3 space-y-2">
          <div class="h-3 rounded-full bg-slate-100 dark:bg-slate-800">
            <div class="h-3 rounded-full bg-gradient-to-r from-cyan-400 to-sky-400" style={`width:${(originalValue / maxValue) * 100}%`}></div>
          </div>
          <div class="h-3 rounded-full bg-slate-100 dark:bg-slate-800">
            <div class="h-3 rounded-full bg-gradient-to-r from-violet to-fuchsia-500" style={`width:${(encryptedValue / maxValue) * 100}%`}></div>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>
