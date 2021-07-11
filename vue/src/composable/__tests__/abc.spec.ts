import { createFetch } from '../createFetch'

const useFetch = createFetch('https://jsonplaceholder.typicode.com')

it('test', async () => {
  const { state, promise } = useFetch('/posts/1').get().json()
  await promise
  console.log(state)
  expect(true).toBe(true)
})
