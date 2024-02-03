using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Monocle;
using MonoMod.Utils;
using System;

namespace Celeste.Mod.WipeColor {
    public partial class WipeColorModule : EverestModule {
        private static void ModifyVertexBuffer(VertexPositionColor[] buf) {
            if (Settings.ModEnabled) {
                for (int i = 0; i < buf.Length; i++) {
                    buf[i].Color = WipeColor;
                }
            }
        }

        private static void AngledWipeHook(On.Celeste.AngledWipe.orig_ctor orig, AngledWipe wipe, Scene scene, bool wipeIn, Action onComplete = null) {
            orig(wipe, scene, wipeIn, onComplete);
            DynData<AngledWipe> data = new DynData<AngledWipe>(wipe);
            ModifyVertexBuffer(data.Get<VertexPositionColor[]>("vertexBuffer"));
        }

        private static void CurtainWipeHook(On.Celeste.CurtainWipe.orig_ctor orig, CurtainWipe wipe, Scene scene, bool wipeIn, Action onComplete = null) {
            orig(wipe, scene, wipeIn, onComplete);
            DynData<CurtainWipe> data = new DynData<CurtainWipe>(wipe);
            ModifyVertexBuffer(data.Get<VertexPositionColor[]>("vertexBufferLeft"));
        }

        private static void DreamWipeHook(On.Celeste.DreamWipe.orig_ctor orig, DreamWipe wipe, Scene scene, bool wipeIn, Action onComplete = null) {
            orig(wipe, scene, wipeIn, onComplete);
            DynData<DreamWipe> data = new DynData<DreamWipe>(wipe);
            ModifyVertexBuffer(data.Get<VertexPositionColor[]>("vertexBuffer"));
        }

        private static void DropWipeHook(On.Celeste.DropWipe.orig_ctor orig, DropWipe wipe, Scene scene, bool wipeIn, Action onComplete = null) {
            orig(wipe, scene, wipeIn, onComplete);
            DynData<DropWipe> data = new DynData<DropWipe>(wipe);
            if (Settings.ModEnabled) data["color"] = WipeColor;
        }

        private static void FallWipeHook(On.Celeste.FallWipe.orig_ctor orig, FallWipe wipe, Scene scene, bool wipeIn, Action onComplete = null) {
            orig(wipe, scene, wipeIn, onComplete);
            DynData<FallWipe> data = new DynData<FallWipe>(wipe);
            ModifyVertexBuffer(data.Get<VertexPositionColor[]>("vertexBuffer"));
        }

        private static void HeartWipeHook(On.Celeste.HeartWipe.orig_ctor orig, HeartWipe wipe, Scene scene, bool wipeIn, Action onComplete = null) {
            orig(wipe, scene, wipeIn, onComplete);
            DynData<HeartWipe> data = new DynData<HeartWipe>(wipe);
            ModifyVertexBuffer(data.Get<VertexPositionColor[]>("vertex"));
        }

        private static void KeyDoorWipeHook(On.Celeste.KeyDoorWipe.orig_ctor orig, KeyDoorWipe wipe, Scene scene, bool wipeIn, Action onComplete = null) {
            orig(wipe, scene, wipeIn, onComplete);
            DynData<KeyDoorWipe> data = new DynData<KeyDoorWipe>(wipe);
            ModifyVertexBuffer(data.Get<VertexPositionColor[]>("vertex"));
        }

        private static void MountainWipeHook(On.Celeste.MountainWipe.orig_ctor orig, MountainWipe wipe, Scene scene, bool wipeIn, Action onComplete = null) {
            orig(wipe, scene, wipeIn, onComplete);
            
            if ((ScreenWipe.WipeColor != Color.White) || Settings.AlwaysReplaceMountainWipe) {
                DynData<MountainWipe> data = new DynData<MountainWipe>(wipe);
                ModifyVertexBuffer(data.Get<VertexPositionColor[]>("vertexBuffer"));
            }
        }

        private static void WindWipeHook(On.Celeste.WindWipe.orig_ctor orig, WindWipe wipe, Scene scene, bool wipeIn, Action onComplete = null) {
            orig(wipe, scene, wipeIn, onComplete);
            DynData<WindWipe> data = new DynData<WindWipe>(wipe);
            ModifyVertexBuffer(data.Get<VertexPositionColor[]>("vertexBuffer"));
        }
    }
}