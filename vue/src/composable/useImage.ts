type ImageShape = [heigt: number, width: number]

export const useImage = {
  getShape: (imageFile: File) =>
    new Promise<ImageShape>((resolve, reject) => {
      const url = URL.createObjectURL(imageFile)
      const image = new Image()
      image.onload = () => {
        resolve([image.naturalHeight, image.naturalWidth])
        URL.revokeObjectURL(url)
      }
      image.src = url
    }),
  getFormat: (imageFile: File) => {
    const parts = imageFile.name.split('.')
    return parts[parts.length - 1]
  }
}
