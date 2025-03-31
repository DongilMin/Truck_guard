import { useEffect, useState } from 'react';
import axios from 'axios';

function FoodtruckList() {
  const [foodtrucks, setFoodtrucks] = useState([]);

  useEffect(() => {
    axios.get(`${import.meta.env.VITE_API_URL}/api/foodtrucks`)
      .then(res => setFoodtrucks(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>🍔 푸드트럭 리스트</h1>
      {foodtrucks.length > 0 ? (
        foodtrucks.map(truck => (
          <div key={truck._id}>
            <h2>{truck.business_name}</h2>
            <p>주소: {truck.address}</p>
            <p>대표자: {truck.ceo_name}</p>
            <p>연락처: {truck.tel_no}</p>
            <hr />
          </div>
        ))
      ) : <p>로딩 중...</p>}
    </div>
  );
}

export default FoodtruckList;
