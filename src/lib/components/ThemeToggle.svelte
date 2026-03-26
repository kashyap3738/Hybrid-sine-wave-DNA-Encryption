<script>
  export let theme = "light";
  export let onToggle = () => {};
</script>

<button
  class="btn-secondary group fixed right-4 top-4 z-50 gap-3 px-4 py-3 shadow-lg shadow-slate-900/5 backdrop-blur md:right-6 md:top-6 dark:shadow-black/20"
  on:click={onToggle}
  aria-label="Toggle color theme"
>
  <span class="relative flex h-6 w-11 items-center rounded-full bg-slate-200 p-1 transition dark:bg-slate-700">
    <span class={`h-4 w-4 rounded-full transition ${theme === "dark" ? "translate-x-5 bg-cyan-300" : "translate-x-0 bg-white"}`}></span>
  </span>
  <span class="text-sm font-semibold">{theme === "dark" ? "Dark" : "Light"} mode</span>
</button>
