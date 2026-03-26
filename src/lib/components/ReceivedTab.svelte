<script>
  export let shares = [];
</script>

<div class="panel p-6">
  <div class="flex items-center justify-between">
    <h3 class="font-display text-lg font-semibold">Received images</h3>
    <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{shares.length}</span>
  </div>

  <div class="table-wrap mt-4">
    <table class="min-w-full text-left text-sm">
      <thead class="text-slate-500 dark:text-slate-400">
        <tr>
          <th class="pb-3 font-medium">Filename</th>
          <th class="pb-3 font-medium">Sender</th>
          <th class="pb-3 font-medium">Shared at</th>
          <th class="pb-3 font-medium">Status</th>
        </tr>
      </thead>
      <tbody>
        {#if shares.length}
          {#each shares as share}
            <tr class="border-t border-slate-100 dark:border-slate-800">
              <td class="py-3 pr-4 font-medium text-slate-900 dark:text-slate-100">{share.filename}</td>
              <td class="py-3 pr-4 text-slate-600 dark:text-slate-300">{share.sender}</td>
              <td class="py-3 pr-4 text-slate-600 dark:text-slate-300">{share.shared_at}</td>
              <td class="py-3 text-slate-600 dark:text-slate-300">
                {#if share.is_expired === 1}
                  Expired
                {:else if share.view_duration}
                  Timer: {share.view_duration}s
                {:else}
                  Ready
                {/if}
              </td>
            </tr>
          {/each}
        {:else}
          <tr>
            <td colspan="4" class="py-6 text-slate-500">No images shared with you yet.</td>
          </tr>
        {/if}
      </tbody>
    </table>
  </div>
</div>
