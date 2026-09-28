import { useLayoutEffect } from 'react'
import type { RefObject } from 'react'

const supportsFieldSizing = () =>
  typeof CSS !== 'undefined' && CSS.supports('field-sizing', 'content')

export function useAutoResize(
  ref: RefObject<HTMLTextAreaElement | null>,
  value: string,
) {
  useLayoutEffect(() => {
    const element = ref.current
    if (!element || supportsFieldSizing()) return
    element.style.height = 'auto'
    element.style.height = `${element.scrollHeight}px`
  }, [ref, value])
}
