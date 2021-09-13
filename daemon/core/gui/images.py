
import logging
from enum import Enum
from typing import Dict, Optional, Tuple

from PIL import Image
from PIL.ImageTk import PhotoImage

from core.api.grpc.wrappers import Node, NodeType
from core.gui.appconfig import LOCAL_ICONS_PATH

NODE_SIZE: int = 48
ANTENNA_SIZE: int = 32
BUTTON_SIZE: int = 16
ERROR_SIZE: int = 24
DIALOG_SIZE: int = 16
IMAGES: Dict[str, str] = {}


def load_all() -> None:
    i = 1
    images = LOCAL_ICONS_PATH.glob("*")
    logging.debug(images)
    for image in images:
        try:
            logging.debug("load image " +str(i)+ ": " + str(image))
            ImageEnum(image.stem)
            IMAGES[image.stem] = str(image)
            i = i + 1
        except ValueError:
            pass


def from_file(
    file_path: str, *, width: int, height: int = None, scale: float = 1.0
) -> PhotoImage:
    if height is None:
        height = width
    width = int(width * scale)
    height = int(height * scale)
    image = Image.open(file_path)
    image = image.resize((width, height), Image.ANTIALIAS)
    return PhotoImage(image)


def from_enum(
    image_enum: "ImageEnum", *, width: int, height: int = None, scale: float = 1.0
) -> PhotoImage:
    file_path = IMAGES[image_enum.value]
    return from_file(file_path, width=width, height=height, scale=scale)


class ImageEnum(Enum):
    SWITCH = "lanswitch"
    CORE = "core-icon"
    START = "start"
    MARKER = "marker"
    ROUTER = "router"
    SELECT = "select"
    LINK = "link"
    HUB = "hub"
    WLAN = "wlan"
    EMANE = "emane"
    RJ45 = "rj45"
    TUNNEL = "tunnel"
    OVAL = "oval"
    RECTANGLE = "rectangle"
    TEXT = "text"
    HOST = "host"
    PC = "pc"
    MDR = "mdr"
    PROUTER = "prouter"
    OVS = "OVS"
    OVSWITCH = "ovswitch"#added at 2021/07/28
    EDITNODE = "edit-node"
    PLOT = "plot"
    TWONODE = "twonode"
    PAUSE = "pause"
    STOP = "stop"
    OBSERVE = "observe"
    RUN = "run"
    DOCUMENTNEW = "document-new"
    DOCUMENTSAVE = "document-save"
    FILEOPEN = "fileopen"
    EDITDELETE = "edit-delete"
    ANTENNA = "antenna"
    DOCKER = "docker"
    LXC = "lxc"
    ALERT = "alert"
    DELETE = "delete"
    SHUTDOWN = "shutdown"
    CANCEL = "cancel"
    ERROR = "error"
    SHADOW = "shadow"


TYPE_MAP: Dict[Tuple[NodeType, str], ImageEnum] = {
    (NodeType.DEFAULT, "ovswitch"): ImageEnum.OVSWITCH,# added at 2021/07/28
    (NodeType.DEFAULT, "router"): ImageEnum.ROUTER,
    (NodeType.DEFAULT, "PC"): ImageEnum.PC,
    (NodeType.DEFAULT, "host"): ImageEnum.HOST,
    (NodeType.DEFAULT, "mdr"): ImageEnum.MDR,
    (NodeType.DEFAULT, "prouter"): ImageEnum.PROUTER,
    (NodeType.HUB, ""): ImageEnum.HUB,
    (NodeType.SWITCH, ""): ImageEnum.SWITCH,
    (NodeType.WIRELESS_LAN, ""): ImageEnum.WLAN,
    (NodeType.EMANE, ""): ImageEnum.EMANE,
    (NodeType.RJ45, ""): ImageEnum.RJ45,
    (NodeType.TUNNEL, ""): ImageEnum.TUNNEL,
    (NodeType.DOCKER, ""): ImageEnum.DOCKER,
    (NodeType.LXC, ""): ImageEnum.LXC,
}


def from_node(node: Node, *, scale: float) -> Optional[PhotoImage]:
    image = None
    image_enum = TYPE_MAP.get((node.type, node.model))
    if image_enum:
        image = from_enum(image_enum, width=NODE_SIZE, scale=scale)
    return image
