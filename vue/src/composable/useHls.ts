import Hls from 'hls.js'
import type { Ref } from 'vue'

export function useHls(video: Ref<HTMLVideoElement>) {
  if (Hls.isSupported()) {
  }
}
