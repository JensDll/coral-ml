import { RecordType } from '~/api'

declare global {
  interface Window {
    onLoadLinks: Record<RecordType, 'image-classification' | 'video-analysis'>
  }

  const JSMpeg: any
}
