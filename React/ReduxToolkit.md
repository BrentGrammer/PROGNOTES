# Redux Toolkit

- Store is made up of multiple slices
- use the PayloadAction type to type action args in reducer fns whenever you are using a payload

```javascript
// store/store.js
// pass the .reducer of the slice to the store prop:
export const store = configureStore({
  reducer: {
    cart: cartSlice.reducer,
  },
});
```

### Creating a slice

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
      const itemIndex = state.items.find(
        (item) => item.id === action.payload.id
      );
      if (itemIndex > 0) {
        // toolkit allows you to write syntax as if directly mutating the state
        state.items[itemIndex].quantity++;
      } else {
        state.items.push({ ...action.payload, quantity: 1 });
      }
    },
    removeFromCart(state, action: PayloadAction<string>) {
      const itemIndex = state.items.find(
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

// export the action creators which you use to dispatch actions in the app:
export const { addToCart, removeFromCart } = cartSlice.actions;
```

### Add extra type info to useDispatch hook: hooks.ts to type dispatch for thunks:

```javascript
// store/store.ts

//...
// add more specific type information about our store to the default useDispatch and useSelector hooks

export type AppDispatch = typeof store.dispatch; // adds more information on which type of actions can be dispatched
// use the Return typescript helper utility to get the return value of getState() and use that type
export type RootState = ReturnType<typeof store.getState>;
```

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

    const cartItems = useAppSelector((state) => state.cart.items)

    const handleClick = () => {
      dispatch(addToCart({ id: "123", title: "title", price: 1.0 }));
    };
  }
  ```
