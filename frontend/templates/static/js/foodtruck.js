// static/js/foodtrucks.js
const API_BASE_URL = 'http://localhost:8000';
let currentPage = 1;
let searchTerm = '';

// 페이지 로드시 실행
document.addEventListener('DOMContentLoaded', function() {
    // 초기 푸드트럭 목록 로드
    loadFoodtrucks();
    
    // 검색 기능 설정
    setupSearch();
    
    // 더보기 버튼 이벤트 설정
    const loadMoreBtn = document.querySelector('#trucks button');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            currentPage++;
            loadFoodtrucks(currentPage, searchTerm, true);
        });
    }
});

// 검색 기능 설정
function setupSearch() {
    const searchInput = document.getElementById('search');
    const searchButton = searchInput.nextElementSibling;
    
    // 검색 버튼 클릭 이벤트
    searchButton.addEventListener('click', () => {
        searchTerm = searchInput.value.trim();
        currentPage = 1;
        loadFoodtrucks(currentPage, searchTerm);
    });
    
    // 엔터키 이벤트
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchTerm = searchInput.value.trim();
            currentPage = 1;
            loadFoodtrucks(currentPage, searchTerm);
        }
    });
}

// 푸드트럭 데이터 로드
async function loadFoodtrucks(page = 1, search = '', append = false) {
    try {
        const params = {
            skip: (page - 1) * 12,
            limit: 12
        };
        
        if (search) {
            params.search = search;
        }
        
        const response = await axios.get(`${API_BASE_URL}/foodtrucks/`, { params });
        const foodtrucks = response.data;
        
        // 데이터 표시
        updateFoodtrucksList(foodtrucks, append);
        
    } catch (error) {
        console.error('푸드트럭 목록을 가져오는데 실패했습니다:', error);
    }
}

// 푸드트럭 목록 업데이트
function updateFoodtrucksList(foodtrucks, append = false) {
    const trucksListContainer = document.getElementById('trucksList');
    
    if (!append) {
        trucksListContainer.innerHTML = '';
    }
    
    // 데이터가 없는 경우
    if (foodtrucks.length === 0 && !append) {
        trucksListContainer.innerHTML = `
            <div class="col-span-full text-center py-10">
                <p class="text-gray-500">검색 결과가 없습니다.</p>
            </div>
        `;
        return;
    }
    
    // 푸드트럭 카드 생성
    foodtrucks.forEach(truck => {
        const card = createFoodtruckCard(truck);
        trucksListContainer.appendChild(card);
    });
    
    // 더보기 버튼 표시/숨김 처리
    const loadMoreBtn = document.querySelector('#trucks button');
    if (loadMoreBtn) {
        loadMoreBtn.style.display = foodtrucks.length < 12 ? 'none' : 'inline-block';
    }
}

// 푸드트럭 카드 생성
function createFoodtruckCard(truck) {
    const card = document.createElement('div');
    card.className = 'truck-card bg-white rounded-lg shadow-md overflow-hidden';
    
    const rating = truck.avg_rating ? truck.avg_rating.toFixed(1) : 'N/A';
    const reviewCount = truck.review_count || 0;
    
    card.innerHTML = `
        <div class="p-6">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-bold">${truck.business_name}</h3>
                <div class="rating">
                    <i class="fas fa-star"></i>
                    <span>${rating}</span>
                </div>
            </div>
            <p class="text-gray-600 mb-4">${truck.address}</p>
            <div class="flex justify-between items-center">
                <span class="text-sm text-gray-500">리뷰 ${reviewCount}개</span>
                <a href="/foodtruck/${truck._id}" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-1 rounded-full text-sm">
                    상세 정보
                </a>
            </div>
        </div>
    `;
    
    // 카드 클릭 이벤트
    card.addEventListener('click', (e) => {
        // 버튼이 아닌 부분 클릭 시 카드 전체를 클릭한 것으로 처리
        if (!e.target.closest('a')) {
            window.location.href = `/foodtruck/${truck._id}`;
        }
    });
    
    return card;
}

// 푸드트럭 상세 정보 로드
async function loadFoodtruckDetail(id) {
    try {
        const response = await axios.get(`${API_BASE_URL}/foodtrucks/${id}`);
        const truck = response.data;
        
        // 상세 정보 표시 함수 호출
        displayFoodtruckDetail(truck);
        
        // 리뷰 로드
        loadReviews(id);
        
    } catch (error) {
        console.error('푸드트럭 상세 정보를 가져오는데 실패했습니다:', error);
    }
}

// 리뷰 로드
async function loadReviews(foodtruckId) {
    try {
        const response = await axios.get(`${API_BASE_URL}/reviews/`, {
            params: { foodtruck_id: foodtruckId }
        });
        
        const reviews = response.data;
        
        // 리뷰 표시
        displayReviews(reviews);
        
    } catch (error) {
        console.error('리뷰를 가져오는데 실패했습니다:', error);
    }
}

// 리뷰 제출
async function submitReview(foodtruckId, rating, comment) {
    try {
        // 실제 서비스에서는 인증이 필요함
        const userId = 'anonymous'; // 임시 사용자 ID
        
        const reviewData = {
            foodtruck_id: foodtruckId,
            user_id: userId,
            rating: rating,
            comment: comment
        };
        
        const response = await axios.post(`${API_BASE_URL}/reviews/`, reviewData);
        
        // 리뷰 다시 로드
        loadReviews(foodtruckId);
        
        return true;
    } catch (error) {
        console.error('리뷰 제출에 실패했습니다:', error);
        return false;
    }
}