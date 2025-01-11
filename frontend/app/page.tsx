"use client";

import clsx from "clsx";
import { useState } from "react";

import { Button, Field, Input, Label, Transition } from "@headlessui/react";

export default function Home() {
  const [open, setOpen] = useState(false);

  return (
    <div className="p-4">
      <form>
        <ul role="list">
          <li className="flex justify-between py-4">
            <ul role="list">
              <li className="flex justify-between py-1">
                <Field>
                  <Label className="text-sm/6 font-medium text-white">
                    馬名
                  </Label>
                  <Input
                    className={clsx(
                      "mt-3 block w-full rounded-lg border-none bg-white/5 py-1.5 px-3 text-sm/6 text-white",
                      "focus:outline-none data-[focus]:outline-2 data-[focus]:-outline-offset-2 data-[focus]:outline-white/25"
                    )}
                  />
                </Field>
              </li>
              <li className="flex justify-between py-1">
                <Field>
                  <Label className="text-sm/6 font-medium text-white">
                    レース名
                  </Label>
                  <Input
                    className={clsx(
                      "mt-3 block w-full rounded-lg border-none bg-white/5 py-1.5 px-3 text-sm/6 text-white",
                      "focus:outline-none data-[focus]:outline-2 data-[focus]:-outline-offset-2 data-[focus]:outline-white/25"
                    )}
                  />
                </Field>
              </li>
            </ul>
          </li>
          <li className="flex justify-between py-4">
            <Button
              className="rounded bg-sky-600 py-2 px-4 text-sm text-white data-[hover]:bg-sky-500 data-[active]:bg-sky-700"
              onClick={() => setOpen(true)}
            >
              評判を見る
            </Button>
          </li>
          <li className="flex justify-between py-4">
            <Transition show={open}>
              <div className="transition duration-300 ease-in data-[closed]:opacity-0">
                強い馬だと思います！
              </div>
            </Transition>
          </li>
        </ul>
      </form>
    </div>
  );
}
