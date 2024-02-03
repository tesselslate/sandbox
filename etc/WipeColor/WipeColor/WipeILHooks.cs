using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Mono.Cecil.Cil;
using MonoMod.Cil;
using System.Reflection;
using System;

namespace Celeste.Mod.WipeColor {
    public partial class WipeColorModule : EverestModule {
        private static FieldInfo WipeColorField = typeof(WipeColorModule).GetField("WipeColor", BindingFlags.Public | BindingFlags.Static);

        private static Color GetWipeColor() {
            if (Settings.ModEnabled) return WipeColor;
            else return Color.Black;
        }

        private static void FadeRenderHook(ILContext context) {
            ILCursor cursor = new ILCursor(context);

            while (cursor.TryGotoNext(MoveType.After, instr => instr.MatchLdsfld("Celeste.ScreenWipe", "WipeColor"))) {
                Logger.Log("WipeColor/FadeRender", $"Applying wipe color hook to {cursor.Index} in {cursor.Method.FullName}");

                cursor.Index--;
                cursor.Remove();
                cursor.EmitDelegate<Func<Color>>(GetWipeColor);
            }
        }

        private static void HeartRenderHook(ILContext context) {
            ILCursor cursor = new ILCursor(context);

            while (cursor.TryGotoNext(MoveType.After, instr => instr.MatchLdsfld("Celeste.ScreenWipe", "WipeColor"))) {
                Logger.Log("WipeColor/HeartRender", $"Applying wipe color hook to {cursor.Index} in {cursor.Method.FullName}");

                cursor.Index--;
                cursor.Remove();
                cursor.EmitDelegate<Func<Color>>(GetWipeColor);
            }
        }

        private static void SpotlightRenderHook(ILContext context) {
            ILCursor cursor = new ILCursor(context);
            
            while (cursor.TryGotoNext(MoveType.After, instr => instr.MatchLdsfld("Celeste.ScreenWipe", "WipeColor"))) {
                Logger.Log("WipeColor/SpotlightRender", $"Applying wipe color hook to {cursor.Index} in {cursor.Method.FullName}");

                cursor.Index--;
                cursor.Remove();
                cursor.EmitDelegate<Func<Color>>(GetWipeColor);
            }
        }

        private static void StarfieldRenderHook(ILContext context) {
            ILCursor cursor = new ILCursor(context);

            while (cursor.TryGotoNext(MoveType.After, instr => instr.MatchLdsfld("Celeste.StarfieldWipe", "SubtractBlendmode"))) {
                Logger.Log("WipeColor/StarfieldRender", $"Applying blendstate hook to {cursor.Index} in {cursor.Method.FullName}");

                cursor.Prev.Operand = typeof(BlendState).GetField("AlphaBlend", BindingFlags.Public | BindingFlags.Static);
            }

            while (cursor.TryGotoNext(MoveType.After, 
                instr => instr.OpCode == OpCodes.Ldsfld,
                instr => instr.OpCode == OpCodes.Ldnull,
                instr => instr.OpCode == OpCodes.Ldnull,
                instr => instr.OpCode == OpCodes.Ldnull)) 
            {
                Logger.Log("WipeColor/StarfieldRender", $"Applying effect hook to {cursor.Index} in {cursor.Method.FullName}");

                cursor.Index--;
                cursor.Remove();
                cursor.Emit(OpCodes.Ldsfld, typeof(WipeColorModule).GetField("StarfieldEffect", BindingFlags.Public | BindingFlags.Static));
            }
        }
    }
}