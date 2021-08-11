import { DirectiveBinding, Plugin } from 'vue'

// @ts-ignore
interface MyDirectiveBinding<TValue = any, TArg = any>
  extends DirectiveBinding<TValue> {
  arg: TArg
}

export const longPress: Plugin = {
  install(app) {
    const sleep = (ms: number) =>
      new Promise<void>((resolve, reject) => {
        setTimeout(() => {
          resolve()
        }, ms)
      })

    let isDown = false

    const onDown = (binding: MyDirectiveBinding<() => void, string | number>) =>
      function (this: HTMLElement, e: MouseEvent | TouchEvent) {
        e.stopPropagation()
        e.preventDefault()

        const box = {
          isDown: true
        }

        setTimeout(async () => {
          while (true) {
            if (box.isDown) {
              await sleep(50)
              binding.value()
            } else {
              break
            }
          }
        }, +binding.arg)

        const onUp = (e: MouseEvent | TouchEvent) => {
          box.isDown = false
          window.removeEventListener('mouseup', onUp)
          this.removeEventListener('touchend', onUp)
        }

        window.addEventListener('mouseup', onUp)
        this.addEventListener('touchend', onUp)
      }

    app.directive('long-press', {
      mounted(el: HTMLElement, binding) {
        if (!binding.arg) {
          binding.arg = 175 as any
        }
        el.addEventListener('mousedown', onDown(binding as any))
        el.addEventListener('touchstart', onDown(binding as any))
      },
      beforeUnmount(el: HTMLElement, binding) {
        el.removeEventListener('mousedown', onDown(binding as any))
        el.removeEventListener('touchstart', onDown(binding as any))
      }
    })
  }
}
