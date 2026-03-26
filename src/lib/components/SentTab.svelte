<script>
  export let data = { images: [], shared_history: [] };
</script>

<div class="grid gap-6 lg:grid-cols-2">
  <div class="panel p-6">
    <div class="flex items-center justify-between">
      <h3 class="font-display text-lg font-semibold">Encrypted images</h3>
      <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{data.images.length}</span>
    </div>
    <div class="table-wrap mt-4">
      <table class="min-w-full text-left text-sm">
        <thead class="text-slate-500 dark:text-slate-400">
          <tr>
            <th class="pb-3 font-medium">Filename</th>
            <th class="pb-3 font-medium">Uploaded</th>
          </tr>
        </thead>
        <tbody>
          {#if data.images.length}
            {#each data.images as image}
              <tr class="border-t border-slate-100 dark:border-slate-800">
                <td class="py-3 pr-4 font-medium text-slate-900 dark:text-slate-100">{image.filename}</td>
                <td class="py-3 text-slate-600 dark:text-slate-300">{image.uploaded_at}</td>
              </tr>
            {/each}
          {:else}
            <tr>
              <td colspan="2" class="py-6 text-slate-500">No encrypted images yet.</td>
            </tr>
          {/if}
        </tbody>
      </table>
    </div>
  </div>

  <div class="panel p-6">
    <div class="flex items-center justify-between">
      <h3 class="font-display text-lg font-semibold">Sharing history</h3>
      <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{data.shared_history.length}</span>
    </div>
    <div class="table-wrap mt-4">
      <table class="min-w-full text-left text-sm">
        <thead class="text-slate-500 dark:text-slate-400">
          <tr>
            <th class="pb-3 font-medium">Filename</th>
            <th class="pb-3 font-medium">Shared with</th>
            <th class="pb-3 font-medium">Shared at</th>
          </tr>
        </thead>
        <tbody>
          {#if data.shared_history.length}
            {#each data.shared_history as share}
              <tr class="border-t border-slate-100 dark:border-slate-800">
                <td class="py-3 pr-4 font-medium text-slate-900 dark:text-slate-100">{share.filename}</td>
                <td class="py-3 pr-4 text-slate-600 dark:text-slate-300">{share.shared_with}</td>
                <td class="py-3 text-slate-600 dark:text-slate-300">{share.shared_at}</td>
              </tr>
            {/each}
          {:else}
            <tr>
              <td colspan="3" class="py-6 text-slate-500">No shares yet.</td>
            </tr>
          {/if}
        </tbody>
      </table>
    </div>
  </div>
</div>
