export function useDownload(file: Blob, filename: string) {
  const a = document.createElement("a")

  a.href = URL.createObjectURL(file)
  a.download = filename
  a.click()

  URL.revokeObjectURL(a.href)
}
