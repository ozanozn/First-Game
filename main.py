from pygame import *
from random import randint

# Pygame'i başlat
init()

# Arka plan müziği
mixer.init()
mixer.music.load('space.ogg')  # Arka plan müziği dosyasını yükle
mixer.music.play()  # Arka plan müziğini çal
fire_sound = mixer.Sound('fire.ogg')  # Ateş sesi dosyasını yükle

# Resim dosyaları
img_back = "galaxy.jpg"  # Arka plan resmi
img_hero = "rocket.png"  # Kahraman (oyuncu) resmi
img_enemy = "ufo.png"  # Düşman resmi
img_bullet = "bullet.png"  # Mermi resmi

# sprite'lar için ebeveyn sınıfı
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))  # Resmi yeniden boyutlandır
        self.speed = player_speed  # Hız değerini ata
        self.rect = self.image.get_rect()  # Dikdörtgen alanı al
        self.rect.x = player_x  # X koordinatını ata
        self.rect.y = player_y  # Y koordinatını ata
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  # Resmi ekrana çiz

# Ana oyuncu sınıfı
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()  # Basılı olan tuşları al
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed  # Sol tarafa hareket et
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed  # Sağ tarafa hareket et
    
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)  # Mermi oluştur
        bullets.add(bullet)  # Mermiyi mermi grubuna ekle
        fire_sound.play()  # Ateş sesini çal

# Düşman sınıfı
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed  # Aşağı hareket et
        if self.rect.y > win_height:
            self.rect.y = -50  # Yeniden yukarıya konumlandır
            self.rect.x = randint(80, win_width - 80)  # X konumunu rastgele belirle
            global lost
            lost += 1  # Kaçırılan düşman sayısını arttır

# Mermi sınıfı
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed  # Yukarı hareket et
        if self.rect.y < 0:
            self.kill()  # Ekranın dışına çıkan mermiyi yok et

# Oyun değişkenlerini başlat
win_width = 700  # Pencere genişliği
win_height = 500  # Pencere yüksekliği
display.set_caption("Shooter")  # Pencere başlığı
window = display.set_mode((win_width, win_height))  # Pencere boyutları
background = transform.scale(image.load(img_back), (win_width, win_height))  # Arka planı yeniden boyutlandır ve yükle

# Sprite'ları oluştur
def create_sprites():
    global ship, monsters, bullets, lost, score
    ship = Player(img_hero, 5, win_height-100, 80, 100, 10)  # Oyuncu karakterini oluştur
    monsters = sprite.Group()  # Düşmanlar grubu
    for i in range(1, 6):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))  # Düşman oluştur
        monsters.add(monster)  # Düşmanı gruba ekle
    bullets = sprite.Group()  # Mermiler grubu
    lost = 0  # Kaçırılan düşman sayısı
    score = 0  # Skor

create_sprites()

# Oyun bitiş değişkenleri
finish = False  # Oyun bitiş durumu
run = True  # Oyun döngüsü durumu

# Oyunu sıfırlama fonksiyonu
def reset_game():
    global finish
    create_sprites()  # Sprite'ları yeniden oluştur
    finish = False  # Oyun bitiş durumunu sıfırla

# Ana oyun döngüsü
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False  # Oyunu kapat
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                ship.fire()  # Ateş et
            elif e.key == K_r and finish:
                reset_game()  # Oyunu yeniden başlat

    if not finish:
        window.blit(background, (0, 0))  # Arka planı çiz
        ship.update()  # Oyuncuyu güncelle
        monsters.update()  # Düşmanları güncelle
        bullets.update()  # Mermileri güncelle

        ship.reset()  # Oyuncuyu ekrana çiz
        monsters.draw(window)  # Düşmanları ekrana çiz
        bullets.draw(window)  # Mermileri ekrana çiz

        # Çarpışmaları kontrol et
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1  # Skoru arttır
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))  # Yeni düşman oluştur
            monsters.add(monster)  # Yeni düşmanı gruba ekle

        # Skoru ve kaçırılan düşman sayısını çiz
        text = font.Font(None, 36).render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font.Font(None, 36).render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # Oyunun bitip bitmediğini kontrol et
        if lost >= 5:
            finish = True  # Oyun bitti
            text = font.Font(None, 72).render("You lost!", 1, (255, 0, 0))
            window.blit(text, (win_width // 3, win_height // 3))
            text_restart = font.Font(None, 36).render("Press R to restart", 1, (201, 255, 255))
            window.blit(text_restart, (win_width // 3, win_height // 2))

        display.update()  # Ekranı güncelle
    
    time.delay(50)  # 50 milisaniye bekle
