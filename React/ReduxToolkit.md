# Redux Toolkit

- Repos with examples:

  - [Task app](https://github.com/stevekinney/supertasker)
  - [Jetsetter](https://github.com/stevekinney/jetsetter-rtk)

- Store is made up of multiple slices
- use the PayloadAction type to type action args in reducer fns whenever you are using a payload

## Creating a Store

```javascript
// store/store.js
import { configureStore } from "@reduxjs/toolkit";

// pass the .reducer of the slice to the store prop:
export const store = configureStore({
  reducer: {
    cart: cartSlice.reducer,
  },
});
```

## Creating a slice

```javascript
// store/cart-slice.ts
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
// (use PayloadAction to further type action arg in reducer functions)

// create a type describing type of data slice should manage
type CartItem = {
  id: string,
  title: string,
  price: number,
  quantity: number,
};

type CartState = {
  items: CartItem[],
};

// usually it is recommended to make state an object even if you only need a list to start with - this offers flexibility in the future to add keys to the state.
const initialState: CartState = {
  items: [],
};

export const cartSlice = createSlice({
  // give slice a name to uniquely identify it
  name: "cart",
  initialState,
  reducers: {
    // add functions to handle state and data - can name them whatever you want.
    // accepts state and action args. assign payloadaction type from redux to the action argument (only needed if action has extra data/payload)
    addToCart(
      state,
      action: PayloadAction<{ id: string, title: string, price: number }> // this types the payload property
    ) {
      const itemIndex = state.items.findIndex(
        (item) => item.id === action.payload.id
      );
      if (itemIndex > 0) {
        // toolkit allows you to write syntax as if directly mutating the state
        state.items[itemIndex].quantity++;
      } else {
        state.items.push({ ...action.payload, quantity: 1 });
      }
    },
    // NOTE: if you use the syntax as shown with Type['prop'], if that type every changes in a refactor you won't have to update this (as opposed to using PayloadAction<string> for example)
    removeFromCart(state, action: PayloadAction<CartItem["id"]>) {
      const itemIndex = state.items.findIndex(
        (item) => item.id === action.payload // payload is the id string
      );
      if (state.items[itemIndex].quantity === 1) {
        state.items.splice(itemIndex, 1);
      } else {
        state.items[itemIndex].quantity--;
      }
    },
  },
});

// export the actions which you use to dispatch actions in the app:
export const { addToCart, removeFromCart } = cartSlice.actions;

// optionally export the reducer to pass into store.js as cartReducer instead of cartSlice.reducer:
export const cartReducer = cartSlice.reducer;
```

### Add extra type info to useDispatch hook: hooks.ts to type dispatch for thunks and typing state in useSelector():

```javascript
// store/store.ts

//...
const store = configureStore({ ...yourreducers });
// add more specific type information about our store to the default useDispatch and useSelector hooks

export type AppDispatch = typeof store.dispatch; // adds more information on which type of actions can be dispatched
// use the Return typescript helper utility to get the return value of getState() and use that type
export type RootState = ReturnType<typeof store.getState>;
```

### Recommended pattern for using selector and dispatch with typescript:

```javascript
// store/hooks.ts
import {
  useDispatch,
  useSelector,
  type TypedUseSelectorHook,
} from "react-redux";
import { AppDispatch, RootState } from "./store.ts";

// assign a new function type to the AppDispatch type you created in store.ts
type DispatchFunction = () => AppDispatch;

// name a custom hook and assign it to the standard useDispatch hook:
// this adds extra type information to the original dispatch hook
const useAppDispatch: DispatchFunction = useDispatch;
// this version of useSelector is aware of the specific type of data in our store
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

### Dispatching actions

- You don't need to create action types - redux toolkit creates types and objects for you
- use the `slice.actions` to return an object that returns functions matching those in your reducer

  - these functions returned create action objects that can be sent to redux, just use the functions when you need to dispatch actions
  - the slice.actions is called in your slice file and you export the functions from there

  ```javascript
  import { useAppDispatch } from "../store/hooks.ts";

  function Component() {
    // use the custom typed version of useDispatch
    const dispatch = useAppDispatch();

    const cartItems = useAppSelector((state) => state.cart.items);

    const handleClick = () => {
      dispatch(addToCart({ id: "123", title: "title", price: 1.0 }));
    };
  }
  ```

### Async Thunks

- [Example of real world app usage](https://github.com/replayio/devtools/blob/b9e0e68d667ef1b9c8017f2fa85b78a84831db2b/src/devtools/client/debugger/src/reducers/ast.ts)
- Suggestion to use RTKQuery as default option for fetching data with thunks

## Use Builder over Slice when creating a reducer

- Gives you better typescript hints and recommended way
- See [video](https://frontendmasters.com/courses/advanced-redux/create-reducer/) at timestamp 2:35

```javascript
// counter-reducer.ts

// create action
const increment = createAction("INCREMENT", (amount: number) => {
  return {
    payload: amount,
  };
});

// first arg is initial state, second is the builder to add cases (i.e. in a switch statement for ex.)
// state is a WriteableDraft which is a copy of state (you can mutate it directly and immer will resolve for you)
export const counterReducer = createReducer({ count: 0 }, (builder) => {
  // note that you do not need to provide a default case (unless for some custom reason) - builder automatically handles the default case if no action matched.

  // pass in the action from actionCreater - auto typed etc.
  builder.addCase(increment, (state, action) => {
    // we don't return anything here, just change the state
    state.count += action.payload;
  });

  // ... more builder.addCase()s ...
});
```

### Redux toolkit comes with nanoid

- You can use the builtin nanoid package to create ids if needed on the frontend:

```javascript
type DraftTask = Partial<Task>; // create partial so you can make a function to create a full built entity

const createTask = (draftTask: DraftTask): Task => {
  return { ...draftTask, id: nanoid() }; // import from redux toolkit
};
```

## Unit testing

- Everything is functions which makes it easy to test. Pass something in and expect an output.

```javascript
// tasks-slice.test.ts

// we want to get the reducer and the actions
import { tasksReducer, addTask, removeTask } from "./tasks-slice";

describe("tasksSlice", () => {
  // create initial state
  const initialState = {
    entities: [
      createTask({ title: "Write tests" }),
      createTask({ title: "Make them pass" }),
    ],
  };
  it(`should add a task when the ${addTask}`, () => {
    const task = createTask({ title: "Profit" }); // helper that you could define in the slice file in source code which you use in the reducer
    const action = addTask(task);
    const newState = tasksReducer(initialState, action);
    // (the reducer unshifts the task in the reducer)
    expect(newState.entities).toEqual([task, ...initialState.entities]);
  });
});
```
