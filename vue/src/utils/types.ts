type UnPromise<T extends Promise<any>> = T extends Promise<infer TP>
  ? TP
  : never

export type PlainFormData<T extends () => Promise<any>> = UnPromise<
  ReturnType<T>
>
