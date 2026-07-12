"""Tests del runner de webcam del Hito A.1."""

from app.camera_preview import compute_fps, run_camera_preview


class _FakeCapture:
    def __init__(self, open_ok: bool = True) -> None:
        self._open_ok = open_ok
        self.released = False
        self._read_count = 0

    def isOpened(self) -> bool:  # noqa: N802
        return self._open_ok

    def set(self, _prop: int, _value: int) -> None:
        return None

    def read(self) -> tuple[bool, str]:
        self._read_count += 1
        return True, f"frame-{self._read_count}"

    def release(self) -> None:
        self.released = True


class _FakeCv2:
    CAP_PROP_FRAME_WIDTH = 3
    CAP_PROP_FRAME_HEIGHT = 4
    WINDOW_NORMAL = 0
    FONT_HERSHEY_SIMPLEX = 0
    LINE_AA = 0

    def __init__(self, capture: _FakeCapture, wait_key_value: int) -> None:
        self._capture = capture
        self._wait_key_value = wait_key_value
        self.destroy_called = False
        self.named_window_called = False

    def VideoCapture(self, _index: int) -> _FakeCapture:  # noqa: N802
        return self._capture

    def namedWindow(self, _window_name: str, _flags: int) -> None:  # noqa: N802
        self.named_window_called = True

    def moveWindow(self, _window_name: str, _x: int, _y: int) -> None:  # noqa: N802
        return None

    def startWindowThread(self) -> None:  # noqa: N802
        return None

    def putText(self, *args: object, **kwargs: object) -> None:  # noqa: N802
        return None

    def imshow(self, _window_name: str, _frame: str) -> None:
        return None

    def waitKey(self, _delay: int) -> int:  # noqa: N802
        return self._wait_key_value

    def destroyAllWindows(self) -> None:  # noqa: N802
        self.destroy_called = True


def test_compute_fps_returns_zero_when_delta_is_invalid() -> None:
    assert compute_fps(1.0, 1.0) == 0.0
    assert compute_fps(2.0, 1.5) == 0.0


def test_run_camera_preview_closes_resources_on_quit_key() -> None:
    capture = _FakeCapture(open_ok=True)
    cv2 = _FakeCv2(capture=capture, wait_key_value=ord("q"))

    run_camera_preview(cv2_module=cv2)

    assert cv2.named_window_called is True
    assert capture.released is True
    assert cv2.destroy_called is True


def test_run_camera_preview_raises_when_camera_cannot_open() -> None:
    capture = _FakeCapture(open_ok=False)
    cv2 = _FakeCv2(capture=capture, wait_key_value=ord("q"))

    try:
        run_camera_preview(cv2_module=cv2)
        assert False, "Se esperaba RuntimeError"
    except RuntimeError as exc:
        assert "No se pudo abrir la webcam" in str(exc)
