import React, {useState} from "react";
import {Button, Spinner} from "evergreen-ui";
import "./App.css";

function App() {
   const [resp, setResp] = useState(null);
   const [loading, setLoading] = useState(false);
   const [gen, setGen] = useState("standard");
   
   const handleGenSwitch = async () => {
      if (gen === "standard"){
         setGen("random")
      }
      else {
         setGen("standard")
      }
   }


   const handleClick = async () => {
      setResp(null);
      setLoading(true);
      try {
         const response = await fetch(`http://127.0.0.1:5000/?gen=${gen}`);
         const respJSON = await response.json();
         setLoading(false);
         setResp(respJSON);
         Object.keys(respJSON.paras).forEach((k) => console.log(respJSON.paras[k]))
         console.log(respJSON)
      } catch (error) {
         console.log("error")
         console.log(error)
         setLoading(false);
         setResp({"msg": error.message, "paras": null});
      }
   };
   
   let paraItems = []
   const getParaItems = (paras) => {
      console.log(paras)
      Object.keys(paras).forEach(para => {
         paraItems.push(<div className="para" key={para}>{paras[para]}</div>)
         paraItems.push(<></>)
      })

      return paraItems
   }
      
   return (
      <div className="App">
         <h1 className="title">Artificial Band Biography Generator</h1>
         <p className="subtitle">Ishaan, James, Arman, Mani</p>
         <div className="topcorner" >
            <Button appearance="secondary" height={40} onClick={handleGenSwitch}>{gen === "standard" ? "Mix N' Match" : "Standard"}</Button>
         </div>

         {loading && (<Spinner className="spinner" />)}
         {resp && (
            <>
            <h2>{resp.band_name}</h2>
            {/* <p>The server returned</p> */}
            {resp.paras && getParaItems(resp.paras)}
            <p className="srvmsg">{resp.msg}</p>
            </>
         )}
            
         <div className="btn" >
            <Button appearance="primary" height={40} onClick={handleClick}>Generate!</Button>
         </div>
         
      </div>
   );
}
            
export default App;
            