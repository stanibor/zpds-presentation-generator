from pptx import Presentation
import numpy as np
import torchaudio
import torch
from pathlib import Path
from os import PathLike
from speechbrain.pretrained import Tacotron2, HIFIGAN

from typing import List

DEFAULT_SAMPLING_RATE = 22050

def get_pretrained_tacotron(tmpdir: Path = Path("")):
    # prepare temporary directories for model weights and metadata
    tmpdir = Path(tmpdir)
    tmpdir_vocoder = tmpdir / "vocoder"
    tacotron_model = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir=tmpdir_vocoder)
    return tacotron_model


def get_pretrained_hifi_gan(tmpdir: Path = Path("")):
    # prepare temporary directories for model weights and metadata
    tmpdir = Path(tmpdir)
    tmpdir_tts = tmpdir / "tts"
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir=tmpdir_tts)
    return hifi_gan


def get_pretrained_tts_models(tmpdir: Path = Path("")):
    tacotron_model = get_pretrained_tacotron(tmpdir)
    hifi_gan = get_pretrained_hifi_gan(tmpdir)
    return tacotron_model, hifi_gan


def extract_presentation_notes(presentation: Presentation) -> List[str]:
    notes = [slide.notes_slide.notes_text_frame.text for slide in presentation.slides]
    return notes


def synthesize_spoken_notes(slide_notes: List[str], tacotron_model, hifi_gan) -> List[torch.Tensor]:
    sorter = np.argsort([len(x) for x in slide_notes])[::-1]  # sort notes in descending order
    inv_sorter = np.argsort(sorter)  # inverse sorter
    items = np.array(slide_notes)[sorter]  # it is required by tacotron batched inference function
    mel_outputs, mel_lengths, alignments = tacotron_model.encode_batch(items)
    waveforms = hifi_gan.decode_batch(mel_outputs)
    lens = mel_lengths.div(mel_lengths.max()).mul_(waveforms.shape[-1]).ceil_().long()
    wavs = [waveforms[i, :, :lens[i]] for i in inv_sorter]  # cut each clip at its lenghts

    return wavs


def save_full_speech(wavs: List[torch.Tensor],
                     output_path: Path = Path("full_speech.wav"),
                     pause_time=0.5,
                     sampling_rate = DEFAULT_SAMPLING_RATE):
    pause = wavs[0].new_zeros(1, int(pause_time * sampling_rate))
    wavs_pauses = [item for wav in wavs for item in [wav, pause]]
    big_wav = torch.cat(wavs_pauses, dim=-1)
    torchaudio.save(output_path, big_wav, sampling_rate)


def save_waveforms(wavs: List[torch.Tensor], output_dir=Path(""), sampling_rate=DEFAULT_SAMPLING_RATE):
    output_dir = Path(output_dir)
    audio_tracks = []
    for i, wav in enumerate(wavs):
        audio_track = output_dir / f"S{i}.wav"
        torchaudio.save(str(audio_track), wav, sampling_rate)
        audio_tracks.append(str(audio_track))

    return audio_tracks


def annotate_presentation_with_spoken_notes(presentation: Presentation, audio_tracks: List[PathLike]) -> Presentation:
    assert len(audio_tracks) <= len(presentation.slides)
    for i, audio_track in enumerate(audio_tracks):
        slide = presentation.slides[i]
        slide.shapes.add_movie(audio_track, 0, 0, 100, 100)

    return presentation

