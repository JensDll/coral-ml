type ImageShape = [heigt: number, width: number]

export function useImage(imageFile: File) {
  return {
    getShape: () =>
      new Promise<ImageShape>((resolve, reject) => {
        const url = URL.createObjectURL(imageFile)
        const image = new Image()
        image.onload = () => {
          resolve([image.naturalHeight, image.naturalWidth])
          URL.revokeObjectURL(url)
        }
        image.src = url
      }),
    getFormat: () => {
      const parts = imageFile.name.split('.')
      return parts[parts.length - 1]
    }
  }
}
