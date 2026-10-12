import { deleteE2eAccounts } from "./support";

export default function globalTeardown() {
  deleteE2eAccounts();
}
