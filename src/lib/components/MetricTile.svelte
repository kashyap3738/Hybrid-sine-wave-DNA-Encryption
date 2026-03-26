<script>
  export let label = "";
  export let value = "";
  export let hint = "";
  export let accent = "cyan";

  const accents = {
    cyan: "from-cyan-500/15 to-blue-500/10 text-cyan-700 dark:text-cyan-300",
    violet: "from-violet-500/15 to-fuchsia-500/10 text-violet-700 dark:text-violet-300",
    coral: "from-coral/15 to-orange-500/10 text-orange-700 dark:text-orange-300",
    emerald: "from-emerald-500/15 to-teal/10 text-emerald-700 dark:text-emerald-300"
  };
</script>

<div class={`rounded-3xl bg-gradient-to-br ${accents[accent] || accents.cyan} border border-black/5 p-5 dark:border-white/5`}>
  <div class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500 dark:text-slate-400">{label}</div>
  <div class="mt-3 text-3xl font-semibold">{value}</div>
  {#if hint}
    <p class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{hint}</p>
  {/if}
</div>
