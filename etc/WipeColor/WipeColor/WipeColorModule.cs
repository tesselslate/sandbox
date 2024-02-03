using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Monocle;
using System;

namespace Celeste.Mod.WipeColor {
    public partial class WipeColorModule : EverestModule {
        public static WipeColorModule Instance;
    
        public override Type SettingsType => typeof(WipeColorSettings);
        public static WipeColorSettings Settings => (WipeColorSettings) Instance._Settings;

        public static Color WipeColor = Color.Black;

        public static Effect StarfieldEffect;

        public WipeColorModule() {
            Instance = this;
        }

        public override void Load() {
            ApplyClearColor();

            // Wipe constructors
            On.Celeste.AngledWipe.ctor += AngledWipeHook;
            On.Celeste.CurtainWipe.ctor += CurtainWipeHook;
            On.Celeste.DreamWipe.ctor += DreamWipeHook;
            On.Celeste.DropWipe.ctor += DropWipeHook;
            On.Celeste.FallWipe.ctor += FallWipeHook;
            On.Celeste.HeartWipe.ctor += HeartWipeHook;
            On.Celeste.KeyDoorWipe.ctor += KeyDoorWipeHook;
            On.Celeste.MountainWipe.ctor += MountainWipeHook;
            On.Celeste.WindWipe.ctor += WindWipeHook;

            // Extra hooks
            IL.Celeste.FadeWipe.Render += FadeRenderHook;
            IL.Celeste.HeartWipe.Render += HeartRenderHook;
            IL.Celeste.SpotlightWipe.Render += SpotlightRenderHook;
            IL.Celeste.StarfieldWipe.Render += StarfieldRenderHook;

            On.Celeste.Editor.MapEditor.ctor += MapEditorCtorHook;
            On.Celeste.Editor.MapEditor.MakeMapEditorBetter += MapEditorBetterHook;
            On.Celeste.Editor.MapEditor.Update += MapEditorUpdateHook;

            On.Celeste.LevelEnter.Go += LevelEnterGoHook;
            On.Celeste.IntroVignette.End += IntroVignetteFinishHook;
            On.Celeste.SummitVignette.Update += SummitVignetteUpdateHook;
            On.Celeste.CoreVignette.StartGame += CoreVignetteFinishHook;
            On.Celeste.CoreVignette.ReturnToMap += CoreVignetteRtmHook;
        }

        public override void Unload() {
            // Wipe constructors
            On.Celeste.AngledWipe.ctor -= AngledWipeHook;
            On.Celeste.CurtainWipe.ctor -= CurtainWipeHook;
            On.Celeste.DreamWipe.ctor -= DreamWipeHook;
            On.Celeste.DropWipe.ctor -= DropWipeHook;
            On.Celeste.FallWipe.ctor -= FallWipeHook;
            On.Celeste.HeartWipe.ctor -= HeartWipeHook;
            On.Celeste.KeyDoorWipe.ctor -= KeyDoorWipeHook;
            On.Celeste.MountainWipe.ctor -= MountainWipeHook;
            On.Celeste.WindWipe.ctor -= WindWipeHook;

            // Extra hooks
            IL.Celeste.FadeWipe.Render -= FadeRenderHook;
            IL.Celeste.HeartWipe.Render -= HeartRenderHook;
            IL.Celeste.SpotlightWipe.Render -= SpotlightRenderHook;
            IL.Celeste.StarfieldWipe.Render -= StarfieldRenderHook;

            On.Celeste.Editor.MapEditor.ctor -= MapEditorCtorHook;
            On.Celeste.Editor.MapEditor.MakeMapEditorBetter -= MapEditorBetterHook;
            On.Celeste.Editor.MapEditor.Update -= MapEditorUpdateHook;

            On.Celeste.LevelEnter.Go -= LevelEnterGoHook;
            On.Celeste.IntroVignette.End -= IntroVignetteFinishHook;
            On.Celeste.SummitVignette.Update -= SummitVignetteUpdateHook;
            On.Celeste.CoreVignette.StartGame -= CoreVignetteFinishHook;
            On.Celeste.CoreVignette.ReturnToMap -= CoreVignetteRtmHook;
        }

        public override void LoadContent(bool firstLoad) {
            ModAsset starfieldFx = Everest.Content.Get("StarfieldShader.cso", true);
            if (starfieldFx == null) {
                Logger.Log(LogLevel.Error, "WipeColor", "Failed to load starfield pixel shader from mod");
            } else {
                try {
                    StarfieldEffect = new Effect(Engine.Graphics.GraphicsDevice, starfieldFx.Data);
                    StarfieldEffect.Parameters["WipeColor"].SetValue(new Vector4(WipeColorModule.WipeColor.R / 255f, WipeColorModule.WipeColor.G / 255f, WipeColorModule.WipeColor.B / 255f, WipeColorModule.WipeColor.A / 255f));
                    Logger.Log("WipeColor", "Registered pixel shader as effect");
                } catch (Exception e) {
                    Logger.Log(LogLevel.Error, "WipeColor", "Failed to create starfield pixel shader");
                    Logger.LogDetailed(e);
                }
            }
        }

        public static void ApplyClearColor() {
            if (Settings.BackgroundEnabled && Settings.ModEnabled) {
                Monocle.Engine.ClearColor = WipeColor;
            } else {
                Monocle.Engine.ClearColor = Color.Black;
            }
        }
    }
}