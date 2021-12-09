import { acceptHMRUpdate, defineStore } from 'pinia'

export type DrawerType = 'edit' | 'create'

export const useDrawerStore = defineStore('drawer', () => {
  /**
   * Current open state of the drawer.
   */
  const drawerOpen = ref<Record<DrawerType, boolean>>({ edit: false, create: false })

  /**
   * Change the current open state of the drawer.
   *
   * @param type - type of drawer
   * @param open - whether open or close the drawer
   */
  function setDrawerOpen(type: DrawerType, open: boolean) {
    drawerOpen.value = { edit: false, create: false }
    switch (type) {
      case 'edit':
        drawerOpen.value.edit = open
        break
      case 'create':
        drawerOpen.value.create = open
        break
    }
  }

  return { drawerOpen, setDrawerOpen }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useDrawerStore, import.meta.hot))
