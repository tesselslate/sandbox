using Celeste.Editor;
using Microsoft.Xna.Framework;
using Monocle;
using MonoMod.Utils;
using System;

namespace Celeste.Mod.WipeColor {
    public partial class WipeColorModule : EverestModule {
        private static void MapEditorCtorHook(On.Celeste.Editor.MapEditor.orig_ctor orig, MapEditor self, AreaKey area, bool reloadMapData = true) {
            orig(self, area, reloadMapData);

            if (!Settings.ApplyToDebugMap) {
                Engine.ClearColor = Color.Black;
            }
        }

        private static void MapEditorBetterHook(On.Celeste.Editor.MapEditor.orig_MakeMapEditorBetter orig, MapEditor self) {
            orig(self);
            DynData<Engine> data = new DynData<Engine>(Engine.Instance);

            if (data.Get<Scene>("nextScene").GetType() == typeof(LevelLoader)) {
                ApplyClearColor();
            }
        }

        private static void MapEditorUpdateHook(On.Celeste.Editor.MapEditor.orig_Update orig, MapEditor self) {
            orig(self);
            DynData<Engine> data = new DynData<Engine>(Engine.Instance);

            if (data.Get<Scene>("nextScene").GetType() == typeof(LevelLoader)) {
                ApplyClearColor();
            }
        }

        private static void LevelEnterGoHook(On.Celeste.LevelEnter.orig_Go orig, Session session, bool fromSaveData) {
            orig(session, fromSaveData);

            DynData<Engine> data = new DynData<Engine>(Engine.Instance);
            Type sceneType = data.Get<Scene>("nextScene").GetType();

            if (sceneType == typeof(IntroVignette) || sceneType == typeof(SummitVignette) || sceneType == typeof(CoreVignette)) {
                Engine.ClearColor = Color.Black;
            }
        }

        private static void IntroVignetteFinishHook(On.Celeste.IntroVignette.orig_End orig, IntroVignette self) {
            orig(self);
            ApplyClearColor();
        }

        private static void SummitVignetteUpdateHook(On.Celeste.SummitVignette.orig_Update orig, SummitVignette self) {
            orig(self);

            DynData<Engine> data = new DynData<Engine>(Engine.Instance);
            if (data.Get<Scene>("nextScene").GetType() == typeof(LevelLoader)) {
                ApplyClearColor();
            }
        }

        private static void CoreVignetteFinishHook(On.Celeste.CoreVignette.orig_StartGame orig, CoreVignette self) {
            orig(self);
            ApplyClearColor();
        }

        private static void CoreVignetteRtmHook(On.Celeste.CoreVignette.orig_ReturnToMap orig, CoreVignette self) {
            orig(self);
            ApplyClearColor();
        }
    }
}