import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom


def random_guid():
    """
    Returns a GUID formatted like:
    '00 00 00 00 3F 76 B7 04 32 0B 00 00 68 A1 4F AA'
    (16 bytes, uppercase hex, space separated)
    """
    u = uuid.uuid4().bytes
    return " ".join(f"{b:02X}" for b in u)


def prettify_xml(elem):
    """Return pretty-printed XML string."""
    rough_string = ET.tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")


def create_grandma3_timecode(
    filename,
    duration,
    event_times,
    sequence_number=101,
    timecode_name="markers"
):
    """
    Create a grandMA3 timecode XML file.

    Parameters:
        filename (str): Output XML filename
        duration (float): Total duration (seconds)
        event_times (list[float]): List of timestamps for events
        sequence_number (int): Sequence number (e.g., 101)
        timecode_name (str): Name of the timecode
    """

    root = ET.Element("GMA3", DataVersion="1.4.0.2")

    timecode = ET.SubElement(
        root,
        "Timecode",
        Name=timecode_name,
        Guid=random_guid(),
        Cursor="00.00",
        Duration=f"{duration:.3f}",
        LoopCount="0",
        TCSlot="-1",
        SwitchOff="Keep Playbacks",
        Goto="as Go",
        Timedisplayformat="<10d11h23m45>",
        FrameReadout="<Seconds>"
    )

    # First TrackGroup
    trackgroup1 = ET.SubElement(timecode, "TrackGroup", Play="", Rec="")

    ET.SubElement(
        trackgroup1,
        "MarkerTrack",
        Name="Marker",
        Guid=random_guid()
    )

    track = ET.SubElement(
        trackgroup1,
        "Track",
        Guid=random_guid(),
        Target=f"ShowData.DataPools.Default.Sequences.Sequence {sequence_number}",
        Play="",
        Rec=""
    )

    timerange = ET.SubElement(
        track,
        "TimeRange",
        Guid=random_guid(),
        Play="",
        Rec=""
    )

    cmdsubtrack = ET.SubElement(timerange, "CmdSubTrack")

    # Create events
    for i, t in enumerate(event_times, start=1):

        cmdevent = ET.SubElement(
            cmdsubtrack,
            "CmdEvent",
            Name="Go+",
            Time=f"{t:.3f}"
        )

        ET.SubElement(
            cmdevent,
            "RealtimeCmd",
            Type="Key",
            Source="Original",
            UserProfile="0",
            Status="On",
            IsRealtime="1",
            IsXFade="0",
            IgnoreFollow="0",
            IgnoreCommand="0",
            Assert="0",
            IgnoreNetwork="0",
            FromTriggerNode="0",
            IgnoreExecTime="0",
            IssuedByTimecode="0",
            FromLocalHardwareFader="1",
            ExecToken="Go+",
            ValCueDestination=f"ShowData.DataPools.Default.Sequences.Sequence {sequence_number}. {i}"
        )

    # Second empty TrackGroup (as in your example)
    trackgroup2 = ET.SubElement(timecode, "TrackGroup", Play="", Rec="")
    ET.SubElement(
        trackgroup2,
        "MarkerTrack",
        Name="Marker",
        Guid=random_guid()
    )

    # Write file
    xml_string = prettify_xml(root)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"File written: {filename}")
