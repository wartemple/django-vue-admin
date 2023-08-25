import { request } from '@/api/service'
export const urlPrefix = '/api/label/dataset/'

export function GetList (query, limit, page) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: { query, limit, page }
  })
}

export function AddObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}
