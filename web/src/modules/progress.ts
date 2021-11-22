/* eslint-disable no-console */
import { UserModule } from '~/types'

export const install: UserModule = ({ isClient, router }) => {
  if (isClient) {
    router.beforeEach(() => console.log('start progress'))
    router.afterEach(() => console.log('end progress'))
  }
}
