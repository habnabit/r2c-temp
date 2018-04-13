export type DocId = string;
export type DocList = DocId[];
export type User = string;

export interface Doc {
  content: string;
  youAreOwner: boolean;
  otherUsers: User[];
}

export interface OkResponse {
  ok: boolean;
}

export interface NewOwnerPostBody {
  newOwner: User;
}

export interface UserResponse {
  user: User;
}

export interface NewDocPostBody {
  content: string;
}

export interface NewDocResponse {
  created: boolean;
  id?: string;
}
