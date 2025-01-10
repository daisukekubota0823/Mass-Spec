/* Copyright (C) 1997-2007  The Chemistry Development Kit (CDK) project
 *
 * Contact: cdk-devel@lists.sourceforge.net
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation; either version 2.1
 * of the License, or (at your option) any later version.
 * All we ask is that proper credit is given for our work, which includes
 * - but is not limited to - adding the above copyright notice to the beginning
 * of your source code files, and to any copyright notice that you may distribute
 * with programs based on this work.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 */

using NCDK.Graphs;
using NCDK.Tools.Manipulator;
using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace NCDK.StructGen
{
    /// <summary>
    /// The VicinitySampler is a generator of constitutional isomers. It needs to be
    /// provided with a starting constitution and it makes random moves in
    /// constitutional space from there. This generator was first suggested by
    /// Faulon <token>cdk-cite-FAU96</token>.
    /// </summary>
    // @cdk.keyword  structure generator
    // @cdk.module   structgen
    // @cdk.bug      1632610
    public static class VicinitySampler
    {
        /// <summary>
        /// Choose any possible quadruple of the set of atoms
        /// in ac and establish all of the possible bonding schemes according to
        /// Faulon's equations.
        /// </summary>
        public static IEnumerable<IAtomContainer> Sample(IAtomContainer ac)
        {
            Debug.WriteLine("RandomGenerator->Mutate() Start");

            int nrOfAtoms = ac.Atoms.Count;
            double a11 = 0, a12 = 0, a22 = 0, a21 = 0;
            double b11 = 0, lowerborder = 0, upperborder = 0;
            double b12 = 0;
            double b21 = 0;
            double b22 = 0;
            double[] cmax = new double[4];
            double[] cmin = new double[4];
            IAtomContainer newAc = null;

            IAtom ax1 = null, ax2 = null, ay1 = null, ay2 = null;
            IBond b1 = null, b2 = null, b3 = null, b4 = null;
            //int[] choices = new int[3];
            /* We need at least two non-zero bonds in order to be successful */
            int nonZeroBondsCounter = 0;
            for (int x1 = 0; x1 < nrOfAtoms; x1++)
            {
                for (int x2 = x1 + 1; x2 < nrOfAtoms; x2++)
                {
                    for (int y1 = x2 + 1; y1 < nrOfAtoms; y1++)
                    {
                        for (int y2 = y1 + 1; y2 < nrOfAtoms; y2++)
                        {
                            nonZeroBondsCounter = 0;
                            ax1 = ac.Atoms[x1];
                            ay1 = ac.Atoms[y1];
                            ax2 = ac.Atoms[x2];
                            ay2 = ac.Atoms[y2];

                            /* Get four bonds for these four atoms */

                            b1 = ac.GetBond(ax1, ay1);
                            if (b1 != null)
                            {
                                a11 = BondManipulator.DestroyBondOrder(b1.Order);
                                nonZeroBondsCounter++;
                            }
                            else
                            {
                                a11 = 0;
                            }

                            b2 = ac.GetBond(ax1, ay2);
                            if (b2 != null)
                            {
                                a12 = BondManipulator.DestroyBondOrder(b2.Order);
                                nonZeroBondsCounter++;
                            }
                            else
                            {
                                a12 = 0;
                            }

                            b3 = ac.GetBond(ax2, ay1);
                            if (b3 != null)
                            {
                                a21 = BondManipulator.DestroyBondOrder(b3.Order);
                                nonZeroBondsCounter++;
                            }
                            else
                            {
                                a21 = 0;
                            }

                            b4 = ac.GetBond(ax2, ay2);
                            if (b4 != null)
                            {
                                a22 = BondManipulator.DestroyBondOrder(b4.Order);
                                nonZeroBondsCounter++;
                            }
                            else
                            {
                                a22 = 0;
                            }
                            if (nonZeroBondsCounter > 1)
                            {
                                // Compute the range for b11 (see Faulons formulae for details)

                                cmax[0] = 0;
                                cmax[1] = a11 - a22;
                                cmax[2] = a11 + a12 - 3;
                                cmax[3] = a11 + a21 - 3;
                                cmin[0] = 3;
                                cmin[1] = a11 + a12;
                                cmin[2] = a11 + a21;
                                cmin[3] = a11 - a22 + 3;
                                lowerborder = MathTools.Max(cmax);
                                upperborder = MathTools.Min(cmin);
                                for (b11 = lowerborder; b11 <= upperborder; b11++)
                                {
                                    if (b11 != a11)
                                    {

                                        b12 = a11 + a12 - b11;
                                        b21 = a11 + a21 - b11;
                                        b22 = a22 - a11 + b11;
                                        Debug.WriteLine("Trying atom combination : " + x1 + ":" + x2 + ":" + y1 + ":" + y2);
                                        newAc = (IAtomContainer)ac.Clone();
                                        Change(newAc, x1, y1, x2, y2, b11, b12, b21, b22);
                                        if (ConnectivityChecker.IsConnected(newAc))
                                        {
                                            yield return newAc;
                                        }
                                        else
                                        {
                                            Debug.WriteLine("not connected");
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            yield break;
        }

        private static IAtomContainer Change(IAtomContainer ac, int x1, int y1, int x2, int y2, double b11, double b12,
                double b21, double b22)
        {
            IAtom ax1 = null, ax2 = null, ay1 = null, ay2 = null;
            IBond b1 = null, b2 = null, b3 = null, b4 = null;
            try
            {
                ax1 = ac.Atoms[x1];
                ax2 = ac.Atoms[x2];
                ay1 = ac.Atoms[y1];
                ay2 = ac.Atoms[y2];
            }
            catch (Exception exc)
            {
                Debug.WriteLine(exc);
            }
            b1 = ac.GetBond(ax1, ay1);
            b2 = ac.GetBond(ax1, ay2);
            b3 = ac.GetBond(ax2, ay1);
            b4 = ac.GetBond(ax2, ay2);
            if (b11 > 0)
            {
                if (b1 == null)
                {
                    Debug.WriteLine("no bond " + x1 + "-" + y1 + ". Adding it with order " + b11);
                    b1 = ac.Builder.NewBond(ax1, ay1, BondManipulator.CreateBondOrder(b11));
                    ac.Bonds.Add(b1);
                }
                else
                {
                    b1.Order = BondManipulator.CreateBondOrder(b11);
                    Debug.WriteLine("Setting bondorder for " + x1 + "-" + y1 + " to " + b11);
                }
            }
            else if (b1 != null)
            {
                ac.Bonds.Remove(b1);
                Debug.WriteLine("removing bond " + x1 + "-" + y1);
            }

            if (b12 > 0)
            {
                if (b2 == null)
                {
                    Debug.WriteLine("no bond " + x1 + "-" + y2 + ". Adding it with order " + b12);
                    b2 = ac.Builder.NewBond(ax1, ay2, BondManipulator.CreateBondOrder(b12));
                    ac.Bonds.Add(b2);
                }
                else
                {
                    b2.Order = BondManipulator.CreateBondOrder(b12);
                    Debug.WriteLine("Setting bondorder for " + x1 + "-" + y2 + " to " + b12);
                }
            }
            else if (b2 != null)
            {
                ac.Bonds.Remove(b2);
                Debug.WriteLine("removing bond " + x1 + "-" + y2);
            }

            if (b21 > 0)
            {
                if (b3 == null)
                {
                    Debug.WriteLine("no bond " + x2 + "-" + y1 + ". Adding it with order " + b21);
                    b3 = ac.Builder.NewBond(ax2, ay1, BondManipulator.CreateBondOrder(b21));
                    ac.Bonds.Add(b3);
                }
                else
                {
                    b3.Order = BondManipulator.CreateBondOrder(b21);
                    Debug.WriteLine("Setting bondorder for " + x2 + "-" + y1 + " to " + b21);
                }
            }
            else if (b3 != null)
            {
                ac.Bonds.Remove(b3);
                Debug.WriteLine("removing bond " + x2 + "-" + y1);
            }

            if (b22 > 0)
            {
                if (b4 == null)
                {
                    Debug.WriteLine("no bond " + x2 + "-" + y2 + ". Adding it  with order " + b22);
                    b4 = ac.Builder.NewBond(ax2, ay2, BondManipulator.CreateBondOrder(b22));
                    ac.Bonds.Add(b4);
                }
                else
                {
                    b4.Order = BondManipulator.CreateBondOrder(b22);
                    Debug.WriteLine("Setting bondorder for " + x2 + "-" + y2 + " to " + b22);
                }
            }
            else if (b4 != null)
            {
                ac.Bonds.Remove(b4);
                Debug.WriteLine("removing bond " + x2 + "-" + y2);
            }
            return ac;
        }
    }
}
