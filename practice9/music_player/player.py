import os
import pygame


class MusicPlayer:
    SUPPORTED_EXTENSIONS = (".mp3", ".wav", ".ogg")

    def __init__(self, music_dir: str):
        pygame.mixer.init()
        self.music_dir = music_dir
        self.tracks: list[str] = self._load_tracks()
        self.current_index: int = 0
        self.is_playing: bool = False
        self.is_stopped: bool = True

    def _load_tracks(self) -> list[str]:
        if not os.path.isdir(self.music_dir):
            return []
        files = sorted(
            f for f in os.listdir(self.music_dir)
            if f.lower().endswith(self.SUPPORTED_EXTENSIONS)
        )
        return [os.path.join(self.music_dir, f) for f in files]

    @property
    def current_track_name(self) -> str:
        if not self.tracks:
            return "Нет треков в папке music/"
        return os.path.basename(self.tracks[self.current_index])

    @property
    def position_seconds(self) -> float:
        if self.is_stopped or not self.tracks:
            return 0.0
        pos_ms = pygame.mixer.music.get_pos()
        return max(0.0, pos_ms / 1000.0)

    def play(self) -> None:
        if not self.tracks:
            return
        if self.is_stopped:
            pygame.mixer.music.load(self.tracks[self.current_index])
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_stopped = False
        elif not self.is_playing:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def pause_or_play(self) -> None:
        if not self.tracks:
            return
        if self.is_stopped:
            self.play()
        elif self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_stopped = True

    def next_track(self) -> None:
        if not self.tracks:
            return
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.is_stopped = True
        self.play()

    def previous_track(self) -> None:
        if not self.tracks:
            return
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.is_stopped = True
        self.play()