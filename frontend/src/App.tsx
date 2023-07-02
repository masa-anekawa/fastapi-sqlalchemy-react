import React from "react";
import axios from "axios";

type dataType = {
  Hello: string;
}

function App() {
  const [data, setData] = React.useState<dataType>();
  // const url = "http://127.0.0.1:8000";
  const url = "https://sleepy-shelf-41955-325a701212b2.herokuapp.com/";

  const GetData = () => {
    axios.get(url).then((res) => {
      setData(res.data);
    });
  };
  return (
    <div>
      <div>ここに処理を書いていきます</div>
      {data ? <div>{data.Hello}</div> : <button onClick={GetData}>データを取得</button>}
    </div>
  );
}

export default App;
