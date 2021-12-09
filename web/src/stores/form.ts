import { acceptHMRUpdate, defineStore } from 'pinia'

export type FormType = 'employee'

const initialFormModel = {
  employee: {
    user: {
      first_name: '',
      last_name: '',
      username: '',
      email: '',
      dob: null as number | null,
      gender: '',
      phone_number: '',
      avatar_image: undefined as string | undefined,
      avatar_url: undefined as string | undefined,
    },
    address: {
      city: '',
      country: '',
      line1: '',
      line2: undefined as string | undefined,
      postal_code: '',
      state: '',
    },
    department: {
      name: '',
      description: undefined as string | undefined,
      created_at: '',
      updated_at: '',
    },
    salary: null as number | null,
    role: '',
    startAt: null as number | null,
    endAt: null as number | null,
  },
}

export type FormModelType = typeof initialFormModel

export const useFormStore = defineStore('form', () => {
  /**
   * Model state of the form
   */
  const formModel = ref<Record<FormType, Record<string, unknown>>>({
    employee: initialFormModel.employee,
  })

  /**
   * Set the state of the form model
   *
   * @param type - type of the form
   * @param model - new state of the form model
   */
  function setFormModel(type: FormType, model: Record<string, unknown>) {
    formModel.value[type] = model
  }

  /**
   * Reset a form model to its initial state
   *
   * @param type - type of the form
   */
  function resetFormModel(type: FormType) {
    formModel.value[type] = initialFormModel[type]
  }

  return { formModel, setFormModel, resetFormModel }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useFormStore, import.meta.hot))
