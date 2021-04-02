import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import { composeWithDevTools } from "redux-devtools-extension";
import {
  userLoginReducer,
  userRegisterReducer,
  userProfileUpdateReducer,
  userPasswordUpdateReducer,
} from "./reducers/userReducers";


import {
  clustersListReducer,
  subjectsListReducer,
  messagesListReducer,
  messageAddReducer,
  messageEditReducer,
  subjectAddReducer,
} from "./reducers/forumReducers";

const reducer = combineReducers({
  // Users
  userLogin: userLoginReducer,
  userRegister: userRegisterReducer,
  userProfileUpdate: userProfileUpdateReducer,
  userPasswordUpdate: userPasswordUpdateReducer,

  // Forum
  clustersList: clustersListReducer,
  subjectsList: subjectsListReducer,
  messagesList: messagesListReducer,
  messageAdd: messageAddReducer,
  messageEdit: messageEditReducer,
  subjectAdd: subjectAddReducer,
});

const userInfoFromStorage = localStorage.getItem("userInfo")
  ? JSON.parse(localStorage.getItem("userInfo"))
  : null;

const initialState = {
  userLogin: { userInfo: userInfoFromStorage },
};

const middlewares = [thunk];
const store = createStore(
  reducer,
  initialState,
  composeWithDevTools(applyMiddleware(...middlewares))
);

export default store;
