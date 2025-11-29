# 🚀 Quick Start Guide - Advanced Algorithms

## 5 Phút Để Bắt Đầu

### Bước 1: Chạy Chương Trình
```bash
python main.py
```

### Bước 2: Chọn Chế Độ
```
Main Menu
├─ [PvE] - Bạn vs Bot
└─ [EvE] - Bot vs Bot
```

### Bước 3: Chọn Thuật Toán

**🎯 Gợi Ý Nhanh:**

| Trường Hợp | Thuật Toán | Depth | Thời Gian |
|-----------|-----------|-------|-----------|
| ⚡ Chơi nhanh | AlphaBeta++ | 3 | 0.5-1s |
| ⚙️ Cân bằng | Hybrid | 5 | 5-10s |
| 🏆 Chơi mạnh | Negamax | 6 | 15-25s |

### Bước 4: Chọn Value Pack
- **0**: Cơ bản (nhanh)
- **1**: Tác chiến (cân bằng)
- **2**: Nâng cao (chậm, hay)

### Bước 5: Nhập Tham Số
```
AlphaBeta++: Depth 4-5
Negamax: Depth 5-7
MTD(f): Depth 4-6
Hybrid: Depth 4-6 (tự động)
```

---

## 🎮 Ví Dụ Nhanh

### Ví Dụ 1: Chơi với Bot AlphaBeta++
```
1. Main Menu → PvE
2. Bot Type: AlphaBeta++
3. Value Pack: 1
4. Depth: 4
5. Team: RED
6. Simulate → Chơi!
```

### Ví Dụ 2: Xem 2 Bot Đấu
```
1. Main Menu → EvE
2. Black: AlphaBeta++ (Depth 4)
3. Red: Negamax (Depth 6)
4. Simulations: 1
5. Simulate → Xem trận đấu
```

---

## 📊 So Sánh Nhanh

| Feature | AlphaBeta++ | Negamax | MTD(f) | Hybrid |
|---------|------------|---------|--------|--------|
| Tốc độ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Chất lượng | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Bộ nhớ | Thấp | Cao | Cao | Trung |
| Khó | Dễ | Dễ | Khó | Dễ |

---

## ⚡ Cách Chọn Thuật Toán

### ❓ Bạn muốn gì?

**Tốc độ (< 2s)**
→ Chọn **AlphaBeta++** Depth 3-4

**Cân bằng (5-10s)**
→ Chọn **Hybrid** Depth 5

**Chất lượng (> 15s)**
→ Chọn **Negamax** Depth 6-7

**Chính xác tuyệt đối**
→ Chọn **MTD(f)** Depth 4-5

---

## 🔧 Cấu Hình Preset

### Quick (⚡ 0.5-1s)
```
Algorithm: AlphaBeta++
Value Pack: 0
Depth: 3
```

### Balanced (⚙️ 5-10s)
```
Algorithm: Hybrid
Value Pack: 1
Depth: 5
```

### Strong (🏆 20-30s)
```
Algorithm: Negamax
Value Pack: 2
Depth: 6-7
```

### Tournament (🎖️ 30-60s)
```
Algorithm: MTD(f)
Value Pack: 2
Depth: 5-6
```

---

## 🐛 Nếu Có Lỗi

### ImportError?
```python
# Chắc chắn các file này cùng folder:
✓ advanced_algorithms.py
✓ algorithm_config.py
✓ main.py
✓ game_tree.py
```

### Bot quá chậm?
```
Depth 6 → 4
Value Pack 2 → 0
Chọn AlphaBeta++ thay Negamax
```

### Bot quá yếu?
```
Depth 3 → 5-6
Value Pack 0 → 2
Chọn Negamax thay AlphaBeta++
```

---

## 📚 Tài Liệu Chi Tiết

- **ADVANCED_UPDATE.md** - Tất cả tính năng mới
- **ALGORITHMS_GUIDE.md** - Hướng dẫn chi tiết
- **algorithm_config.py** - Cấu hình & presets
- **OPTIMIZATION_REPORT.md** - Cải tiến hiệu suất

---

## ✨ Các Thuật Toán Có Sẵn

```
1. Minimax - Cơ bản, an toàn
2. MCTS - Khám phá, phức tạp
3. DyMinimax - Thích nghi
4. DeMinimax - Sâu dần
5. ExMinimax - Khoan sâu

6. AlphaBeta++ ⭐ - Nhanh & tốt
7. Negamax ⭐ - Nhanh nhất
8. MTD(f) ⭐ - Chính xác nhất
9. Hybrid ⭐ - Tối ưu nhất
```

---

## 🎯 Khuyến Nghị

1. **Lần đầu chơi?** → Dùng **Hybrid** Depth 5
2. **Muốn tốc độ?** → Dùng **AlphaBeta++** Depth 4
3. **Muốn chất lượng?** → Dùng **Negamax** Depth 6
4. **Muốn so sánh?** → Dùng **EvE** mode

---

**Bắt đầu ngay!** 🎮
