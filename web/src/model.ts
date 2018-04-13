type DocId = string;
type DocList = DocId[];
type User = string;

interface Doc {
  content: string;
  youAreOwner: boolean;
  otherUsers: User[];
}

interface OkResponse {
  ok: boolean;
}

interface NewOwnerPostBody {
  newOwner: User;
}

interface UserResponse {
  user: User;
}

interface NewDocPostBody {
  content: string;
}

interface NewDocResponse {
  created: boolean;
  id?: string;
}
