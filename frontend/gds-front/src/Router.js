import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Main from "./pages/Main";
import Signin from "./pages/Singin";
import Mynewslog from "./pages/Mynewslog";
import Mypage from "./pages/Mypage";
import Signup from "./pages/Signup";
import About from "./pages/About";
import Loading from "./components/Loading/Loading";

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Signin />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Main />} />
        <Route path="/mynewslog" element={<Mynewslog />} />
        <Route path="/mypage" element={<Mypage />} />
        <Route path="/About" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
};

export default Router;