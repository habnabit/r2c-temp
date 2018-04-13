import { User, UserResponse } from './model';

export function getWhoami(): Promise<UserResponse> {
  return fetch('http://localhost:7070/api/whoami').then(data => data.json());
}

export function putWhoami(user: User): Promise<UserResponse> {
  return fetch('http://localhost:7070/api/whoami', { method: 'PUT' }).then(
    data => data.json()
  );
}
