import { createStoreSyncedWithStorage } from './createStore';

type Options = { userInfo: string };
const initialOptions: Options = { userInfo: '' };
export const options = createStoreSyncedWithStorage<Options>({
	key: 'options',
	initialValue: initialOptions
});
