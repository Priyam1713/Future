# Third-party components

Frontend uses React, Vite, Tailwind CSS, Lucide, Radix Slot, class-variance-authority, clsx, tailwind-merge and the shadcn/ui Button pattern. Package versions, sources and integrity records are pinned in `web/package-lock.json`; installed packages retain their license files. A CC0 palm image is bundled solely as a software fixture; attribution is in tests/assets/README.md. Existing engine/source rights remain unchanged.

Optional local intake uses [Ollama 0.40.16](https://github.com/ollama/ollama/releases/tag/v0.40.16), MIT licensed, and [Qwen3-VL-4B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct), Apache-2.0 licensed, through its [Ollama quantization](https://ollama.com/library/qwen3-vl:4b-instruct-q4_K_M). Runtime and weights are downloaded separately, with runtime checksum and installed model digest recorded. Binaries are not distributed in this repository. Bundled runtime/model notices remain with their packages. Pillow 12.3.0 retains its HPND license notices in its installed package.

The Button implementation is adapted from [shadcn/ui](https://github.com/shadcn-ui/ui), MIT, Copyright (c) 2023 shadcn.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
