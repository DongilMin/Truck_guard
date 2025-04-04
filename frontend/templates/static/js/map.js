// static/js/map.js
let map;
let markers = [];
let userMarker;
const API_BASE_URL = 'http://localhost:8000';

// 지도 초기화 함수
function initMap() {
    // Kakao Maps API를 사용한다고 가정
    // 실제로는 Kakao Maps API 키를 발급받아야 합니다
    if (typeof kakao !== 'undefined') {
        const mapContainer = document.getElementById('mapContainer');
        const mapOption = {
            center: new kakao.maps.LatLng(37.5665, 126.9780), // 서울 중심
            level: 5 // 줌 레벨
        };
        
        map = new kakao.maps.Map(mapContainer, mapOption);
        
        // 지도 컨트롤 추가
        const zoomControl = new kakao.maps.ZoomControl();
        map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);
        
        // 현재 위치 버튼 이벤트 추가
        document.getElementById('findMe').addEventListener('click', findMyLocation);
    } else {
        console.error('Kakao Maps API가 로드되지 않았습니다.');
    }
}

// 내 위치 찾기 함수
function findMyLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                // 지도 중심 이동
                const moveLatLng = new kakao.maps.LatLng(lat, lng);
                map.setCenter(moveLatLng);
                map.setLevel(3); // 더 가깝게 줌인
                
                // 내 위치 마커 생성 또는 업데이트
                if (userMarker) {
                    userMarker.setPosition(moveLatLng);
                } else {
                    const userMarkerImage = new kakao.maps.MarkerImage(
                        '/static/images/user-marker.png',
                        new kakao.maps.Size(24, 24)
                    );
                    
                    userMarker = new kakao.maps.Marker({
                        position: moveLatLng,
                        map: map,
                        image: userMarkerImage,
                        zIndex: 10
                    });
                }
                
                // 주변 푸드트럭 찾기
                loadNearbyFoodtrucks(lat, lng);
            },
            (error) => {
                console.error('위치 정보를 가져오는데 실패했습니다:', error);
                alert('위치 정보를 가져오는데 실패했습니다. 권한을 확인해주세요.');
            }
        );
    } else {
        alert('이 브라우저에서는 위치 정보를 지원하지 않습니다.');
    }
}

// 주변 푸드트럭 정보 로드
async function loadNearbyFoodtrucks(lat, lng, distance = 1000) {
    try {
        // 기존 마커 제거
        clearMarkers();
        
        // API 호출
        const response = await axios.get(`${API_BASE_URL}/foodtrucks/nearby/`, {
            params: { lat, lng, distance }
        });
        
        const foodtrucks = response.data;
        
        // 마커 생성
        foodtrucks.forEach(truck => {
            if (truck.location && truck.location.coordinates) {
                const [lng, lat] = truck.location.coordinates;
                addMarker(lat, lng, truck);
            }
        });
        
        // 푸드트럭 목록 업데이트
        updateFoodtrucksList(foodtrucks);
        
    } catch (error) {
        console.error('주변 푸드트럭을 가져오는데 실패했습니다:', error);
    }
}

// 마커 추가 함수
function addMarker(lat, lng, truckData) {
    const position = new kakao.maps.LatLng(lat, lng);
    
    const marker = new kakao.maps.Marker({
        position: position,
        map: map
    });
    
    markers.push(marker);
    
    // 정보창 생성
    const infoContent = `
        <div class="p-3" style="min-width: 200px;">
            <h3 class="font-bold">${truckData.business_name}</h3>
            <p>${truckData.address}</p>
            <div class="flex items-center mt-1">
                <span class="text-yellow-500 mr-1">★</span>
                <span>${truckData.avg_rating ? truckData.avg_rating.toFixed(1) : 'N/A'}</span>
                <span class="text-gray-500 ml-2">(${truckData.review_count || 0})</span>
            </div>
            <div class="mt-2">
                <a href="/foodtruck/${truckData._id}" class="text-blue-500 text-sm">상세 정보</a>
            </div>
        </div>
    `;
    
    const infoWindow = new kakao.maps.InfoWindow({
        content: infoContent
    });
    
    // 마커 클릭 이벤트
    kakao.maps.event.addListener(marker, 'click', function() {
        infoWindow.open(map, marker);
    });
    
    return marker;
}

// 모든 마커 제거
function clearMarkers() {
    for (let i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}

// 페이지 로드 시 실행
window.addEventListener('load', function() {
    // Kakao Maps API 로드 확인 및 지도 초기화
    if (typeof kakao !== 'undefined') {
        initMap();
    } else {
        // API가 없는 경우 로드 (실제로는 API 키 필요)
        const script = document.createElement('script');
        script.src = '//dapi.kakao.com/v2/maps/sdk.js?appkey=YOUR_KAKAO_MAP_API_KEY&libraries=services,clusterer&autoload=false';
        script.onload = function() {
            kakao.maps.load(initMap);
        };
        document.head.appendChild(script);
    }
});