export function useUri() {
  return {
    toUrlParams(obj: Record<string, unknown>) {
      return Object.entries(obj).reduce<string>((uri, [key, value]) => {
        return uri + `&${key}=${value}`
      }, '')
    }
  }
}
